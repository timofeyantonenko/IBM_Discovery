# Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Variables that contains the user credentials to access Twitter API
from IBM_Discovery.twitter_api.settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET
from IBM_Discovery.twitter_api.settings import save_to
from IBM_Discovery.twitter_api.settings import topics
import json


def handle_tweet(tweet):
    # print(tweet)
    with open(save_to, "a") as myfile:
        myfile.write(tweet + ",\n")


def load_tweets(file_name):
    tweets_data = []
    tweets_file = open(file_name, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        handle_tweet(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=topics, async=True)
