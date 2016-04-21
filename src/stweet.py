#Import the necessary methods from tweepy library
#from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
#from tweepy import Stream
import json
import tweepy

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print ( data )
        for line in data:
            try:
                tweets.append(json.loads(line))
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
        print("rtweet.py: ALERT: No credentials.py found")
        api_keys['twitter_consumer_key']    = raw_input("Enter your Twitter API consumer key: ")
        api_keys['twitter_consumer_secret'] = raw_input("Enter your Twitter API consumer secret: ")
        api_keys['twitter_access_token'] = raw_input("Enter your Twitter API access token: ")
        api_keys['twitter_access_token_secret'] = raw_input("Enter your Twitter API access token secret: ")
    except:
        print("rtweet.py: ERROR: unable to import credentials - unknown reason")

    return api_keys

def main ()
    
    # read API Keys
    api_keys = get_credentials()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
 
    return

if __name__ == '__main__':
    main ()

