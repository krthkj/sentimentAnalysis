#!/usr/bin/env python

import os, sys, string, time, re
import requests, json, urllib, urllib2, base64
import pymongo
from multiprocessing import Pool, Lock, Queue, Manager

import random

def get_state():
    state_list = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    return random.choice(state_list)


def get_age():
    return random.randint(18,60)


def main(search_term, num_tweets):

    # Establish credentials for Twitter and AlchemyAPI
    credentials = get_credentials()
    
    # Get the Twitter bearer token
    auth = oauth(credentials)

    # Pull Tweets down from the Twitter API
    raw_tweets = search(search_term, num_tweets, auth)

    # De-duplicate Tweets by ID
    unique_tweets = dedup(raw_tweets)

    # Enrich the body of the Tweets using AlchemyAPI
    enriched_tweets = enrich(credentials, unique_tweets, sentiment_target = search_term)

    # Store data in MongoDB
    store(enriched_tweets)

    return

def get_credentials():
    creds = {}
    creds['consumer_key']    = str()
    creds['consumer_secret'] = str()
    creds['apikey']      = str()

    # If the file credentials.py exists, then grab values from it.
    # Values: "twitter_consumer_key," "twitter_consumer_secret," "alchemy_apikey"
    # Otherwise, the values are entered by the user
    try:
        import credentials
        creds['consumer_key']    = credentials.twitter_consumer_key
        creds['consumer_secret'] = credentials.twitter_consumer_secret
        creds['apikey']          = credentials.alchemy_apikey 
    except:
        print "No credentials.py found"
        creds['consumer_key']    = raw_input("Enter your Twitter API consumer key: ")
        creds['consumer_secret'] = raw_input("Enter your Twitter API consumer secret: ")
        creds['apikey']          = raw_input("Enter your AlchemyAPI key: ")
        
    print "Using the following credentials:"
    print "\tTwitter consumer key:", creds['consumer_key']
    print "\tTwitter consumer secret:", creds['consumer_secret']
    print "\tAlchemyAPI key:", creds['apikey']

    # Test the validity of the AlchemyAPI key
    test_url = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo"
    test_parameters = {"apikey" : creds['apikey'], "outputMode" : "json"}
    test_results = requests.get(url=test_url, params=test_parameters)
    test_response = test_results.json()

    if 'OK' != test_response['status']:
        print "Oops! Invalid AlchemyAPI key (%s)" % creds['apikey']
        print "HTTP Status:", test_results.status_code, test_results.reason
        sys.exit()

    return creds

def oauth(credentials):

    print "Requesting bearer token from Twitter API"

    try:
        # Encode credentials
        encoded_credentials = base64.b64encode(credentials['consumer_key'] + ':' + credentials['consumer_secret'])        
        # Prepare URL and HTTP parameters
        post_url = "https://api.twitter.com/oauth2/token"
        parameters = {'grant_type' : 'client_credentials'}
        # Prepare headers
        auth_headers = {
            "Authorization" : "Basic %s" % encoded_credentials,
            "Content-Type"  : "application/x-www-form-urlencoded;charset=UTF-8"
            }

        # Make a POST call
        results = requests.post(url=post_url, data=urllib.urlencode(parameters), headers=auth_headers)
        response = results.json()

        # Store the access_token and token_type for further use
        auth = {}
        auth['access_token'] = response['access_token']
        auth['token_type']   = response['token_type']

        print "Bearer token received"
        return auth

    except Exception as e:
        print "Failed to authenticate with Twitter credentials:", e
        print "Twitter consumer key:", credentials['consumer_key']
        print "Twitter consumer secret:", credentials['consumer_secret']
        sys.exit()
        

def search(search_term, num_tweets, auth):
    # This collection will hold the Tweets as they are returned from Twitter
    collection = []
    # The search URL and headers
    url = "https://api.twitter.com/1.1/search/tweets.json"
    search_headers = {
        "Authorization" : "Bearer %s" % auth['access_token']
        }
    max_count = 100
    next_results = ''
    # Can't stop, won't stop
    while True:
        print "Search iteration, Tweet collection size: %d" % len(collection)
        count = min(max_count, int(num_tweets)-len(collection))

        # Prepare the GET call
        if next_results:
            get_url = url + next_results
        else:
            parameters = {
                'q' : search_term,
                'count' : count,
                'lang' : 'en'
                } 
            get_url = url + '?' + urllib.urlencode(parameters)

        # Make the GET call to Twitter
        results = requests.get(url=get_url, headers=search_headers)
        response = results.json()

        # Loop over statuses to store the relevant pieces of information
        for status in response['statuses']:
            text = status['text'].encode('utf-8')

            # Filter out retweets
            if status['retweeted'] == True:
                continue
            if text[:3] == 'RT ':
                continue

            # Configure the fields you are interested in from the status object
            status['age'] = get_age()
            status['location'] = get_state()
            status['search_term'] = search_term
            collection += [status]

            if len(collection) >= num_tweets:
                print "Search complete! Found %d tweets" % len(collection)
                return collection

        if 'next_results' in response['search_metadata']:
            next_results = response['search_metadata']['next_results']
        else:
            print "Uh-oh! Twitter has dried up. Only collected %d Tweets (requested %d)" % (len(collection), num_tweets)
            print "Last successful Twitter API call: %s" % get_url
            print "HTTP Status:", results.status_code, results.reason
            return collection

def enrich(credentials, tweets, sentiment_target = ''):
    # Prepare to make multiple asynchronous calls to AlchemyAPI
    apikey = credentials['apikey']
    pool = Pool(processes = 10)
    mgr = Manager()
    result_queue = mgr.Queue()
    # Send each Tweet to the get_text_sentiment function
    for tweet in tweets:
        pool.apply_async(get_text_sentiment, (apikey, tweet, sentiment_target, result_queue))

    pool.close()
    pool.join()
    collection = []
    while not result_queue.empty():
        collection += [result_queue.get()]
    
    print "Enrichment complete! Enriched %d Tweets" % len(collection)
    return collection

def get_text_sentiment(apikey, tweet, target, output):

    # Base AlchemyAPI URL for targeted sentiment call
    alchemy_url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
    
    # Parameter list, containing the data to be enriched
    parameters = {
        "apikey" : apikey,
        "text"   : tweet['text'],
        "outputMode" : "json",
        "showSourceText" : 1
        }

    try:

        results = requests.get(url=alchemy_url, params=urllib.urlencode(parameters))
        response = results.json()

    except Exception as e:
        print "Error while calling TextGetTargetedSentiment on Tweet (ID %s)" % tweet['id']
        print "Error:", e
        return

    try:
        if 'OK' != response['status'] or 'docSentiment' not in response:
            print "Problem finding 'docSentiment' in HTTP response from AlchemyAPI"
            print response
            print "HTTP Status:", results.status_code, results.reason
            print "--"
            return

        tweet['sentiment'] = response['docSentiment']['type']
        tweet['score'] = 0.
        if tweet['sentiment'] in ('positive', 'negative'):
            tweet['score'] = float(response['docSentiment']['score'])
        output.put(tweet)

    except Exception as e:
        print "D'oh! There was an error enriching Tweet (ID %s)" % tweet['id']
        print "Error:", e
        print "Request:", results.url
        print "Response:", response

    return

def dedup(tweets):
    used_ids = []
    collection = []
    for tweet in tweets:
        if tweet['id'] not in used_ids:
            used_ids += [tweet['id']]
            collection += [tweet]
    print "After de-duplication, %d tweets" % len(collection)
    return collection

def store(tweets):
    # Instantiate your MongoDB client
    mongo_client = pymongo.MongoClient()
    # Retrieve (or create, if it doesn't exist) the twitter_db database from Mongo
    db = mongo_client.twitter_db
   
    db_tweets = db.tweets_2

    for tweet in tweets:
        db_id = db_tweets.insert(tweet)
 
    db_count = db_tweets.count()
    
    print "Tweets stored in MongoDB! Number of documents in twitter_db: %d" % db_count

    return


if __name__ == "__main__":

    if not len(sys.argv) == 3:
        print "ERROR: invalid number of command line arguments"
        print "SYNTAX: python recipe.py <SEARCH_TERM> <NUM_TWEETS>"
        print "\t<SEARCH_TERM> : the string to be used when searching for Tweets"
        print "\t<NUM_TWEETS>  : the preferred number of Tweets to pull from Twitter's API"
        sys.exit()

    else:
        main(sys.argv[1], int(sys.argv[2]))
