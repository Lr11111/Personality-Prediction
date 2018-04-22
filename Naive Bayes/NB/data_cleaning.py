import re
from collections import Counter
from collections import defaultdict
tweets_by_id = dict()

word_list = []
regex = re.compile(r'http\S+|@\w+|https\S+|\'+\w+|/|\n|\"+|\.+|[0-9]|\"|\(|\)|\W|\d')
personality = ['ISTJ','ISFJ','INFJ','INTJ','ISTP','ISFP','INFP','INTP','ESTP','ESFP','ENFP','ESFJ','ESTJ','ENFJ','ENTJ','ENTP']
preferences = ['e','i','s','n','t','f','j','p']
# regex2 = re.compile(r'\W|\d["\'\\\]]')
'''
description:read a file and create a dictionary with the userID as key and the user's tweet as a list of value
input:file
output:dictionary
'''
def get_tweets(filename):
    temp= dict()
    with open(filename,'r') as file:
        lines = file.readlines()
        for line in lines:
            user_id =  line.split(" ")[:1][0]
            tweet = line.split(" ")[2:]
            if not user_id in temp:
                temp[user_id] = tweet
            else:temp[user_id]+=tweet
    return temp

'''
description: to clean the tweets
input: dictionary with uncleaned tweets
output: dictionary with cleaned tweets
'''
def clean_data(user_tweet_dict):
    temp_dict = dict()
    for id,value in user_tweet_dict.items():
        temp_list=[]

        for words in value:
            cleaned_word = words.decode('unicode_escape').encode('ascii', 'ignore')
            word = re.sub(regex,'',cleaned_word)
            if len(word)>1:
                temp_list.append(word.lower())
        if not id in temp_dict:
            temp_dict[id]=temp_list
        else:
            temp_dict[id]+=temp_list
    return temp_dict

'''
description: to categorise the personality type of a user by tweet
input: dictionary{user_id:[tweets]}
output: dictionary{user_id:type}
'''

def match_personality(perosonality_tweets_by_id):
    user_personality_dict = dict()

    personality = ['istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp', 'estp',
                   'esfp', 'enfp', 'esfj','estj', 'enfj', 'entj', 'entp']
    for userId,tweet in perosonality_tweets_by_id.items():
        for word in tweet:
            if word in personality:
                user_personality_dict[userId] = word
                break
    return user_personality_dict

def get_count(user_personalityDict,tweets_byId):
    type_wordCount = defaultdict()
    for userId,tweets in tweets_byId.items():
        try:
            types = list(user_personalityDict[userId])
            temp_count = Counter(tweets)
            for word in set(tweets):
                for type in types:
                    if type in type_wordCount:
                        if word in type_wordCount[type]:
                            type_wordCount[type][word] += temp_count[word]
                        else:
                            type_wordCount[type][word] = temp_count[word]
                    else:
                        type_wordCount[type] = {word:temp_count[word]}
        except:
            continue
    return type_wordCount

'''
description: to write the contents of tweets dictionary to a file
'''
def write_file():
    with open('clean.txt','a') as file:
        for user_id,tweet_list in tweets_by_id.items():
            file.write(user_id+" : ")
            for tweet in tweet_list:
                file.write(tweet+" ")
            file.write('\n')


if __name__ == "__main__":
    user_tweets = get_tweets("newusers.txt")
    print user_tweets
    '''a dictionary where key,value is {user_id : [user_tweets]}'''
    tweets_by_id = clean_data(user_tweets)
    #print tweets_by_id
    '''store user_id and user tweets from the file as a dictionary'''
    personality_tweets = get_tweets("FirstTweetsData.txt")

    '''dictionary where key,value is {user_id : [user_tweets]}'''
    perosonality_tweets_by_id = clean_data(personality_tweets)

    ''' user_personalityDict: {type:[user_ids]};
        personality_userDict where key,value is {user_id : type}'''
    user_personalityDict = match_personality(perosonality_tweets_by_id)
    # print personality_userDict

    '''dictionary with key,value as {type:[word:count]}'''
    preferences_wordCount = get_count(user_personalityDict,tweets_by_id)
    #print preferences_wordCount





