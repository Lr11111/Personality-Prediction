#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "920068723960107009-d1ppfYvxGwVWIYijvowJeRQdqzLD8KV"
access_token_secret = "Ra4gHpRGOqlUSFOmbU91snxq4xewBzOQ09FBmOpOJ28iC"
consumer_key = "bHsblsl433krl5140WSKFPiRF"
consumer_secret = "WzFp3J9wPyw0FNTt8sNYXpjM1Mw2yiXLhKO0RvCbMMX4rEIfe3"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(languages=["en"], track=['ESFJ', 'ESTJ', 'ESFP', 'ESTP', 'ISFJ', 'ISTJ', 'ISFP', 'ISTP', 'ENFJ', 'ENTJ', 'ENFP', 'ENTP', 'INFJ','INTJ', 'INFP', 'INTP', 'MyersBriggs', 'MBTI'])


