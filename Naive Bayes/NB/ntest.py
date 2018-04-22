from __future__ import division
from collections import Counter
import math
from data_cleaning import *

def readTweets(file):
    usr = {}
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        line = line.split("::")
        uid = line[0]
        tweets = line[1]
        usr[uid] = tweets
    return usr


def readTweets1(file):
    usr = {}
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        line = line.split("::")
        uid = line[0]
        tweets = line[1]
        usr[uid] = tweets.split()
    return usr


def createTrainDict(filename):
    c = 0
    str = ""
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        c += 1
        line = line.split(" : ")
        tweet = line[1]
        str += tweet
    return str, c


def userWordCount(tweets):
    w = {}
    for user, tweet in tweets.items():
        c = Counter(tweet.split())
        for word in tweet.split():
            if user not in w:
                w[user] = {word:c[word]}
            else:
                w[user].update({word:c[word]})
    return w

def naiveBayes(pos, neg, tweets, V, P, N, fpos, fneg, E, I, user, i):
    truePositive = 0
    falsePositive = 0
    trueNegative = 0
    falseNegative = 0
    u = {}
    pos_nb = 0
    neg_nb = 0
    for uid, tweet in tweets.items():
        c = Counter(tweet)
        words = [word for word, _ in c.most_common(100)]
        for eachWord in words:
            try:
               a = pos[eachWord]
            except:
               a = 0
            x = a+1
            y = P + V
            n = x / y
            pos_nb += math.log(n)
            try:
               e = neg[eachWord]
            except:
               e = 0
            g = e + 1
            h = N + V
            m = g / h
            neg_nb += math.log(m)
        try:
            neg_nb += math.log(fneg)
        except:
            neg_nb += 1
        pos_nb += math.log(fpos)


        if uid in user:
            if user[uid][i] == E and pos_nb >= neg_nb:
                truePositive += 1
                u[uid] = E
            else:
                falsePositive += 1
                u[uid] = I

            if user[uid][i] == I and neg_nb >= pos_nb:
                trueNegative += 1
                u[uid] = I
            else:
                falseNegative += 1
                u[uid] = E
    return u, truePositive, falsePositive, trueNegative, falseNegative

def getWordCount(dict):
    c = 0
    for k in dict.keys():
        c += dict[k]
    return c

def writeDict(filename, dict):
    f = open(filename, "w+")
    for k, v in dict.items():
        f.write(k + "::" + str(v) + "\n")

def getClassCount(file1, file2):
    d1, c1 = createTrainDict(file1)
    d2, c2 = createTrainDict(file2)
    classCount1 = Counter(d1.split())
    classCount2 = Counter(d2.split())
    return classCount1, classCount2, c1, c2

def getEvaluation(x, y, z):
    p = x / (x + y)
    r = x / (x + z)
    try:
        f1 = (2*p*r)/(p+r)
    except:
        f1 = 0
    eval = [p, r, f1]
    return eval

def getTypeUser(user, dict, char, i):
    c = 0
    for k, v in user.items():
        v = dict[k]
        if v[i] == char:
            c += 1
    return c

def compareUsers(d1, d2):
    c = 0
    for k, v in d1.items():
        if k not in d2:
            c += 1
    print c

def printEval(pos):
    print("Precision :" + str(pos[0]))
    print("Recall :" + str(pos[1]))
    print("Positive F1 :" + str(pos[2]))

def getTotalWords(extro, intro):
    c = 0
    for k in extro.keys():
        if k in intro:
            c += 1
    return c

def main():
    user_tweets = readTweets1("trainSet.txt")
    tweets_by_id = clean_data(user_tweets)
    d = {}

    trainData = dict(d.items()[:1000])
    testData = dict(d.items()[1001:])


    #writeDict("trainSet.txt", trainData)
    #writeDict("testSet.txt", testData)

    tweets = readTweets1("testSet.txt")

    personality_tweets = get_tweets("FirstTweetsData.txt")
    perosonality_tweets_by_id = clean_data(personality_tweets)
    user_personalityDict = match_personality(perosonality_tweets_by_id)
    preferences_wordCount = get_count(user_personalityDict, tweets_by_id)
    totalUsers = len(user_tweets)
    uaer = {k: v for k, v in user_personalityDict.iteritems() if k in user_tweets}
    #print len(uaer)

    extro = preferences_wordCount["e"]
    intro = preferences_wordCount["i"]
    eUsers = getTypeUser(user_tweets, user_personalityDict, "e", 0)
    iUsers = getTypeUser(user_tweets, user_personalityDict, "i", 0)
    fex = eUsers / totalUsers
    fin = iUsers / totalUsers
    C = getTotalWords(extro, intro)
    E = getWordCount(extro)
    I = getWordCount(intro)
    V = E + I - C
    c1, tp1, fp1, tn1, fn1 = naiveBayes(extro, intro, tweets, V, E, I, fex, fin, "e", "i", user_personalityDict, 0)
    pos1 = getEvaluation(tp1, fp1, fn1)
    neg1 = getEvaluation(tn1, fn1, fp1)
    #printEval(pos1, neg1)




    sense = preferences_wordCount["s"]
    intuit = preferences_wordCount["n"]
    sUsers = getTypeUser(user_tweets, user_personalityDict, "s", 1)
    inUsers = getTypeUser(user_tweets, user_personalityDict, "n", 1)
    fs = sUsers / totalUsers
    fiu = inUsers / totalUsers
    E = getWordCount(sense)
    I = getWordCount(intuit)
    C = getTotalWords(sense, intuit)
    V = E + I - C
    c2, tp2, fp2, tn2, fn2 = naiveBayes(sense, intuit, tweets, V, E, I, fs, fiu, "s", "n", user_personalityDict, 1)
    pos2 = getEvaluation(tp2, fp2, fn2)
    neg2 = getEvaluation(tn2, fn2, fp2)
    #printEval(pos2, neg2)

    think = preferences_wordCount["t"]
    feel = preferences_wordCount["f"]
    tUsers = getTypeUser(user_tweets, user_personalityDict, "t", 2)
    fUsers = getTypeUser(user_tweets, user_personalityDict, "f", 2)
    ft = tUsers / totalUsers
    ff = fUsers / totalUsers
    E = getWordCount(think)
    I = getWordCount(feel)
    C = getTotalWords(think, feel)
    V = E + I - C
    c3, tp3, fp3, tn3, fn3 = naiveBayes(think, feel, tweets, V, E, I, ft, ff, "t", "f", user_personalityDict, 2)
    pos3 = getEvaluation(tp3, fp3, fn3)
    neg3 = getEvaluation(tn3, fn3, fp3)
    #printEval(pos3, neg3)

    judge = preferences_wordCount["j"]
    persev = preferences_wordCount["p"]
    jUsers = getTypeUser(user_tweets, user_personalityDict, "j", 3)
    pUsers = getTypeUser(user_tweets, user_personalityDict, "p", 3)
    fj = jUsers / totalUsers
    fper = pUsers / totalUsers
    E = getWordCount(judge)
    I = getWordCount(persev)
    C = getTotalWords(judge, persev)
    V = E + I - C
    c4, tp4, fp4, tn4, fn4 = naiveBayes(judge, persev, tweets, V, E, I, fj, fper, "j", "p", user_personalityDict, 3)
    pos4 = getEvaluation(tp4, fp4, fn4)
    neg4= getEvaluation(tn4, fn4, fp4)
    #printEval(pos4, neg4)

    avgTp = tp1 + tp2 + tp3 + tp4
    avgTn = tn1 + tn2 + tn3 + tn4
    avgFp = fp1 + fp2 + fp3 + fp4
    avgFn = fn1 + fn2 + fn3 + fn4
    acc = (avgTp + avgTn)/(avgTp + avgTn + avgFp + avgFn)
    avg = getEvaluation(avgTn, avgFp, avgFn)
    printEval(avg)
    print "Accuary: " + str("{0:.2f}".format(acc*100)) + "%"

main()