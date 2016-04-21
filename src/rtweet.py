#!/usr/bin/env python
# MIT License
#
# Copyright (c) 2016 Karthik Jain <karthikjain@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import requests, json, urllib, urllib2, base64

def file_array(filename):
    # read file to array
    array = []
    with open (filename) as f:
        for line in f:
            array.append(line.rstrip())

    # print (array)
    return array

def main(filename):

    # read array
    searchList = file_array (filename)

    # Get credentials for Twitter
    api_keys = get_credentials()
    auth = oauth (api_keys)
    
    # Pull Tweets down from the Twitter API
    raw_tweet = search(search_term, num_tweets, auth)
    unique_tweet = dedup (raw_tweet)

    store(unique_tweet)
    return

def oauth(api_keys):
    # get twitter API OAuthentication

    try:
        # Encode credentials
        encoded_credentials = base64.b64encode(api_keys['twitter_consumer_key'] + ':' + api_keys['twitter_consumer_secret'])        
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

        print("rtweet.py: Twitter OAuth test = PASS")
        return auth

    except Exception as e:
        print("rtweet.py: Twitter OAuth test = FAIL", e)
        print("Twitter consumer key:", api_keys['twitter_consumer_key'])
        print("Twitter consumer secret:", api_keys['twitter_consumer_secret'])
        sys.exit()

def dedup(tweets):
    used_ids = []
    collection = []
    for tweet in tweets:
        if tweet['id'] not in used_ids:
            used_ids += [tweet['id']]
            collection += [tweet]
    print ("After de-duplication, %d tweets" % len(collection))
    return collection


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

            tweet = {}
            # Configure the fields you are interested in from the status object
            tweet['text']        = text
            tweet['id']          = status['id']
            tweet['time']        = status['created_at'].encode('utf-8')
            tweet['screen_name'] = status['user']['screen_name'].encode('utf-8')
            
            collection    += [tweet]
        
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


def get_credentials():
    # read twitter API from file
    api_keys = {}
    api_keys['twitter_consumer_key']    = ''
    api_keys['twitter_consumer_secret'] = ''

    try:
        import credentials
        api_keys['twitter_consumer_key']    = credentials.twitter_consumer_key
        api_keys['twitter_consumer_secret'] = credentials.twitter_consumer_secret
    except ImportError:
        print("rtweet.py: ALERT: No credentials.py found")
        api_keys['twitter_consumer_key']    = raw_input("Enter your Twitter API consumer key: ")
        api_keys['twitter_consumer_secret'] = raw_input("Enter your Twitter API consumer secret: ")
    except:
        print("rtweet.py: ERROR: unable to import credentials - unknown reason")

    return api_keys

# command line arguments are read from here.
if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("rtweet.py: Reading alternate input file")
        main(sys.argv[1])
    
    elif len (sys.argv) == 1 :
        print("rtweet.py: Reading default input file")
        main('searchMe.txt')

    else:
        print("SYNTAX: python rtweet.py <SEARCH_FILE>")
        print("\t<SEARCH_FILE> : the file which contains the list of string to be used when searching for Tweets")
        sys.exit()

