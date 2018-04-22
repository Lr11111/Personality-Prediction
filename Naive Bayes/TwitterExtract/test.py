import json
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from collections import Counter


access_token = "923010508692885505-cxqDB7uHzAZobOgYWRmZFsacCMlICGh"
access_token_secret = "hht4gssAvDDkKfcp1AjchvgduCi6avODaGsGPaGp5Vnjb"
consumer_key = "BNnrpyoziW66oWlvI6YeqK6NZ"
consumer_secret = "PPvyce4wKpZ6Sa2o2WEVhITMD6qsMyqkGNqrsfja9EMoTMqdry"
user = {}

# Read all tweets from the file and add it to a list
def getTwitterData(dir, path):
    l = []
    for eachFile in dir:
        f = open(path + "\\" + eachFile, 'r')
        lines = f.readlines()
        for index, each in enumerate(lines):
            if (index + 1) % 2 == 1:  # means lines 1, 4 ,7, 10..
                try:
                    tweet = json.loads(each) # load it as Python dict
                except:
                    continue
                l.append(tweet)
    return l

# Create user-tweet dict from the list of tweets
def getUserTweetdata(tweets):
    data = {}
    for tweet in tweets:
        userID = tweet["user"]["id_str"]
        txt = tweet["text"].lower()
        tID = tweet["id_str"]
        lan = tweet["lang"]
        if userID not in data:
            l = []
            l.append(txt)
            data[userID] = l
        else:
            l = data[userID]
            l.append(txt)
    return data

# Return a list of user Ids from the list of tweets
def getUserId(tweets):
    users = []
    for tweet in tweets:
        userID = tweet["user"]["id_str"]
        screen_name = tweet["user"]["screen_name"]
        if userID not in users:
            users.append(userID)
    return users


class StdOutListener(StreamListener):

    def on_data(self, data):
        uid = data["user"]["id"]
        if uid not in user:
            tweetList = []
            tweetList.append(data)
            user[uid] = tweetList
        else:
            tweetList = user[uid]
            tweetList.append(data)
        return user

    def on_error(self, status):
        #print(status)
        return True

# def fetchTweetsForUser(path):
#     d = {}
#     dir = os.listdir(path)
#     for file in dir:
#         f = open(path + "\\" + file, "r")
#         lines = f.readlines()
#         for each in lines:
#             if each != "\n":
#                 each = each.split(":::")
#                 uid = each[0]
#                 tweet = each[1]
#                 print uid, tweet

# Create user-tweet dict from lines of format :
# "userID:::tweet"

def fetchTweetsForUser(path):
    d = {}
    dir = os.listdir(path)
    for file in dir:
        f = open(path + "\\" + file, "r")
        lines = f.readlines()
        for each in lines:
            try:
                if each != "\n":
                    each = each.split(":::")
                    uid = each[0]
                    tweet = each[1]
                    if uid not in d:
                        t = []
                        t.append(tweet)
                        d[uid] = t
                    else:
                        t = d[uid]
                        t.append(tweet)
            except:
                continue
    return d


# write a list to file
def writelist(filename, lst):
    f1 = open(filename, "w+")
    for each in lst:
        f1.write(each + "\n")

# write a dict to file
def writeDict(filename, dict):
    f = open(filename, "w+")
    for k, v in dict.items():
        f.write(k + " " + str(v) + "\n")

def createUsercorpus():
    u = {}
    f = open("cleaned_tweets_byID.txt")
    lines = f.readlines()
    for line in lines:
        line = line.split(" : ")
        uid = line[0]
        tweet = line[1]
        c = Counter(tweet.split())
        for word in tweet.split():
            if uid not in u:
                u[uid] = {word:c[word]}
            else:
                u[uid].update({word:c[word]})
    return u


def main():

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    tpath = "E:\PythonWorkspace\\twitter data\\new"
    path = "E:\PythonWorkspace\Twitterdata"
    n = "E:\PythonWorkspace\\twitter data\\user"
    dir = os.listdir(path)
    tdir = os.listdir(tpath)


    tweets = getTwitterData(tdir, tpath)
    #users = getUserId(tweets)
    #d = fetchTweetsForUser(tpath)
    #writeDict("shashi.txt", d)
    #data = getUserTweetdata(tweets)

    print len(tweets)
    #
    # u = createUsercorpus()
    # #writelist("Users.txt", users)
    # writeDict("FirstTweetsData.txt", data)
    # writeDict("uD.txt", u)
    # print len(u)

main()