#Import the necessary methods from tweepy library
#from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
#from tweepy import Stream
from __future__ import print_function
import json
import tweepy
import pymongo

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        try:
            store(json.loads(data))
        except:
            pass

        return True

    def on_error(self, status):
        print ( status )

def get_credentials():
    # read twitter API from file
    api_keys = {}
    api_keys['twitter_consumer_key']    = ''
    api_keys['twitter_consumer_secret'] = ''
    api_keys['twitter_access_token_secret'] = ''
    api_keys['twitter_access_token'] = ''

    try:
        import credentials
        api_keys['twitter_consumer_key']    = credentials.twitter_consumer_key
        api_keys['twitter_consumer_secret'] = credentials.twitter_consumer_secret
        api_keys['twitter_access_token'] = credentials.twitter_access_token
        api_keys['twitter_access_token_secret'] = credentials.twitter_access_token_secret
    except ImportError:
        print("stweet.py: ALERT: No credentials.py found")
        api_keys['twitter_consumer_key']    = raw_input("Enter your Twitter API consumer key: ")
        api_keys['twitter_consumer_secret'] = raw_input("Enter your Twitter API consumer secret: ")
        api_keys['twitter_access_token'] = raw_input("Enter your Twitter API access token: ")
        api_keys['twitter_access_token_secret'] = raw_input("Enter your Twitter API access token secret: ")
    except:
        print("stweet.py: ERROR: unable to import credentials - unknown reason")

    return api_keys

def store(tweet):
    # Instantiate your MongoDB client
    mongo_client = pymongo.MongoClient()
    # Retrieve (or create, if it doesn't exist) the twitter_db database from Mongo
    db_tweets = mongo_client.twitter_db.tweets_stream
    db_id = db_tweets.insert(tweet)
    db_count = db_tweets.count()
    print("Total tweets streamed in MongoDB: %d" % db_count, end ="\r")
    return

def main ():
    
    # read API Keys
    api_keys = get_credentials()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = tweepy.OAuthHandler(api_keys['twitter_consumer_key'],api_keys['twitter_consumer_secret'])
    auth.set_access_token(api_keys['twitter_access_token'], api_keys['twitter_access_token_secret'])
    stream = tweepy.Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
 
    return

if __name__ == '__main__':
    main ()

