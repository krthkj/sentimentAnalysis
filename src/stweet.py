#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "178344419-BpArn9mWvIgRd0m0wZ83iI52BzgLjR7IVgBCR6Yg"
access_token_secret = "Yj6jijQWx4FWYw6TAhJDEi9lwTbdrcidUNBOBh3IwuR6l"
consumer_key = "cZUYhg1AGiFeERJyk1yEgE5oI"
consumer_secret = "JHkGyWALQNe1avsRYJovsUwqzCY0nWCtG9nFrq0JuNmKbMs0u6"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print ( data )
        return True

    def on_error(self, status):
        print ( status )


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])

