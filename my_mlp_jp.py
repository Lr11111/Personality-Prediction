import tensorflow as tf
from collections import Counter
import time
import numpy as np
import re
from collections import defaultdict
from sklearn.metrics import recall_score, precision_score, f1_score

top_words_by_user = dict()
tweets_by_id = dict()
preferences_wordCount = dict()
word_list = []
regex = re.compile(r'http\S+|@\w+|https\S+|\'+\w+|/|\n|\"+|\.+|[0-9]|\"|\(|\)|\W|\d')
personality = ['ISTJ','ISFJ','INFJ','INTJ','ISTP','ISFP','INFP','INTP','ESTP','ESFP','ENFP','ESFJ','ESTJ','ENFJ','ENTJ','ENTP']
preferences = ['e','i','s','n','t','f','j','p']

# I_tf contains {word: word_freq_in_I_Class}
I_tf = dict()
E_tf = dict()

S_tf = dict()
N_tf = dict()

T_tf = dict()
F_tf = dict()

J_tf = dict()
P_tf = dict()

# dict for userID : PersonalityType
user_type = dict()

# dict for userID : tweetData
# tweetData = {word : word_freq_in_all_tweets}
user_tweets = dict()


def gen_features(tweets, class_1, class_2):
    class_1_count = 0
    class_2_count = 0
    both_class_count = 0
    for w in tweets:
        if w in class_1 and w not in class_2:
            class_1_count += 1

        if w in class_2 and w not in class_1:
            class_2_count += 1

        if w in class_1 and w in class_2:
            both_class_count += 1

    return [class_1_count, class_2_count, both_class_count]


# Generates the review.train and review.test files
# Generated Input Data for the perceptron
def gen_datasets(test_filename, train_filename):
    print "****Generating Data files********"
    fw_test = open("personality.test", "w")
    file = open(test_filename, "r")
    filedata = file.readlines()
    for line in filedata:
        output = ""
        line = line.lower()
        line = line.split(":::")
        tweet = line[0] # top 100 words in tweet
        type = line[1]
        tokens = tweet.split(",")
        top100 = []
        for token in tokens:
            top100.append(token)
        features = gen_features(top100, preferences_wordCount['j'], preferences_wordCount['p'])
        output = str(features[0]) + "," + str(features[1]) + "," + str(features[2]) + ","
        if 'j' in type:
            output += "j" + "\n"
        else:
            output += "p" + "\n"
        fw_test.write(output)
    file.close()
    fw_test.close()

    fw_train = open("personality.train", "w")
    file_2 = open(train_filename, "r")
    filedata_2 = file_2.readlines()
    for line in filedata_2:
        output = ""
        line = line.lower()
        line = line.split(":::")
        tweet = line[0]  # top 100 words from user tweets
        type = line[1]
        tokens = tweet.split(",")
        top100 = []
        for token in tokens:
            top100.append(token)
        features = gen_features(top100, preferences_wordCount['j'], preferences_wordCount['p'])
        output = str(features[0]) + "," + str(features[1]) + "," + str(features[2]) + ","
        if 'j' in type:
            output += "j" + "\n"
        else:
            output += "p" + "\n"
        fw_train.write(output)
    file_2.close()
    fw_train.close()
    print "******Data (Train data + Test data) files Created*********"


# Encode the label
def label_encode(label):
    val = []
    if label == 'j':
        val = [0, 1]
    elif label == 'p':
        val = [1, 0]
    return val


# Encode the input
# Read input from generated Data files
# X => Input
# Y => Label
def data_encode(file):
    X = []
    Y = []
    train_file = open(file, 'r')
    for line in train_file.read().strip().split('\n'):
        line = line.split(',')
        X.append([float(line[0]), float(line[1]), float(line[2])])
        Y.append(label_encode(line[3]))

    return X, Y


# Defining a Multilayer Perceptron Model
# This Model has 1 Hidden layer
def model(x, weights, bias):
    layer_1 = tf.add(tf.matmul(x, weights["hidden"]), bias["hidden"])
    layer_1 = tf.nn.relu(layer_1)

    output_layer = tf.matmul(layer_1, weights["output"]) + bias["output"]
    return output_layer


def clean_data_2(user_tweet_dict):
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


def get_tweets_2(filename):
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

def MLP():
    gen_datasets("tweets.test", "tweets.train")
    start_time = time.time()

    # Training and Testing Data
    train_X, train_Y = data_encode('personality.train')
    test_X, test_Y = data_encode('personality.test')

    # hyperparameter
    learning_rate = 0.01
    training_epochs = 1600
    display_steps = 200

    # Network parameters
    n_input = 3  # Input consists of just three numeric values
    n_hidden = 50  # Number of neurons in hidden layer
    n_output = 2  # Output will have two label (E, I)

    # Graph Nodes
    X = tf.placeholder("float", [None, n_input])
    Y = tf.placeholder("float", [None, n_output])

    # Weights and Biases
    weights = {
        "hidden": tf.Variable(tf.random_normal([n_input, n_hidden]), name="weight_hidden"),
        "output": tf.Variable(tf.random_normal([n_hidden, n_output]), name="weight_output")
    }

    bias = {
        "hidden": tf.Variable(tf.random_normal([n_hidden]), name="bias_hidden"),
        "output": tf.Variable(tf.random_normal([n_output]), name="bias_output")
    }

    # Define model
    pred = model(test_X, weights, bias)


    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=test_Y))
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

    # Initializing global variables
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        print "**********Multilayer Perceptron Configuration*********"
        print "No. of Hidden Layer : 1"
        print "No. of neurons in layer : 25"
        print "Optimizer Used : AdamOptimizer"
        print "******************************************************"
        for epoch in range(training_epochs):
            _, c = sess.run([optimizer, cost], feed_dict={X: train_X, Y: train_Y})
            if (epoch + 1) % display_steps == 0:
                print "Epoch: ", (epoch + 1)    , "Cost: ", c

        print("Optimization Finished!")
        temp = tf.nn.softmax(pred)  # Apply softmax to logits
        correct_prediction = tf.equal(tf.argmax(temp, 1), tf.argmax(Y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        y_p = tf.argmax(pred, 1)
        val_accuracy, y_pred = sess.run([accuracy, y_p], feed_dict={X: test_X, Y: test_Y})

        print "Accuracy:", val_accuracy
        y_true = np.argmax(test_Y, 1)
        print "Precision", precision_score(y_true, y_pred)
        print "Recall", recall_score(y_true, y_pred)
        print "f1_score", f1_score(y_true, y_pred)

    end_time = time.time()

    print "Completed in ", end_time - start_time, " seconds"


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
            user_id = line.split("::")[:1][0]
            tweet = line.split(" ")[2:]
            if user_id not in temp:
                temp[user_id] = tweet
            else:
                temp[user_id].append(tweet)
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

    personality_2 = ['istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp', 'estp',
                   'esfp', 'enfp', 'esfj','estj', 'enfj', 'entj', 'entp']
    for userId,tweet in perosonality_tweets_by_id.items():
        for word in tweet:
            if word in personality_2:
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


if __name__ == '__main__':
    user_tweets = get_tweets("/home/shashikirang/Desktop/data/training data/trainSet.txt")
    #user_tweets = get_tweets("/home/shashikirang/Desktop/data/test data/testSet.txt")
    '''a dictionary where key,value is {user_id : [user_tweets]}'''
    tweets_by_id = clean_data(user_tweets)

    '''store user_id and user tweets from the file as a dictionary'''
    personality_tweets = get_tweets_2("FirstTweetsData.txt")

    '''dictionary where key,value is {user_id : [user_tweets]}'''
    perosonality_tweets_by_id = clean_data_2(personality_tweets)

    ''' user_personalityDict: {type:[user_ids]};
           personality_userDict where key,value is {user_id : type}'''
    user_personalityDict = match_personality(perosonality_tweets_by_id)
    # print personality_userDict

    # fw_train = open("tweets.test", "w")
    # for userID, tweets in tweets_by_id.items():
    #     user_vocab = {}
    #     top_100_words = []
    #     for word in tweets:
    #         if word not in user_vocab:
    #             user_vocab[word] = 1
    #         else:
    #             user_vocab[word] += 1
    #     if len(user_vocab) > 100:
    #         top_100_words = sorted(user_vocab, key=user_vocab.get, reverse=True)[:100]
    #     else:
    #         top_100_words = sorted(user_vocab, key=user_vocab.get, reverse=True)
    #
    #     top_words_by_user[userID] = top_100_words
    #     out = ""
    #     for word in top_100_words:
    #         out += str(word) + ","
    #
    #     out = out[:-1]
    #     out += ":::" + str(user_personalityDict[userID]) + "\n"
    #     fw_train.write(out)
    # fw_train.close()

    '''dictionary with key,value as {type:[word:count]}'''
    preferences_wordCount = get_count(user_personalityDict, tweets_by_id)

    MLP()




