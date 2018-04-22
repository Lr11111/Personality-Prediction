import tensorflow as tf
import time
import numpy as np
import os
from sklearn.metrics import recall_score, precision_score, f1_score


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
        tweet = line[0] # TO DO top 100 words from tweet
        type = line[1]
        tokens = tweet.split(",")
        top100 = []
        for token in tokens:
            top100.append(token)
        features = gen_features(top100, E_tf, I_tf)
        output = str(features[0]) + "," + str(features[1]) + "," + str(features[2]) + ","
        if 'e' in type:
            output += "e" + "\n"
        else:
            output += "i" + "\n"
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
        tweet = line[0]  # TO DO top 100 words from tweet
        type = line[1]
        tokens = tweet.split(",")
        top100 = []
        for token in tokens:
            top100.append(token)
        features = gen_features(top100, E_tf, I_tf)
        output = str(features[0]) + "," + str(features[1]) + "," + str(features[2]) + ","
        if 'e' in type:
            output += "e" + "\n"
        else:
            output += "i" + "\n"
        fw_train.write(output)
    file_2.close()
    fw_train.close()
    print "******Data (Train data + Test data) files Created*********"


gen_datasets("tweets.test", "tweets.train")

start_time = time.time()


# Encode the label
def label_encode(label):
    val = []
    if label == 'e':
        val = [0, 1]
    elif label == 'i':
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
        X.append(line[0])
        X.append(line[1])
        X.append(line[2])
        Y.append(label_encode(line[3]))

    return X, Y


# Defining a Multilayer Perceptron Model
# This Model has 1 Hidden layer
def model(x, weights, bias):
    layer_1 = tf.add(tf.matmul(x, weights["hidden"]), bias["hidden"])
    layer_1 = tf.nn.relu(layer_1)

    output_layer = tf.matmul(layer_1, weights["output"]) + bias["output"]
    return output_layer


# Training and Testing Data
train_X, train_Y = data_encode('personality.train')
test_X, test_Y = data_encode('personality.test')

# hyperparameter
learning_rate = 0.01
training_epochs = 1600
display_steps = 200

# Network parameters
n_input = 2 # Input consists of just two numeric values
n_hidden = 50 # Number of neurons in hidden layer
n_output = 2 # Output will have two label (E, I)

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
pred = model(X, weights, bias)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=Y))
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
            print "Epoch: ", (epoch + 1), "Cost: ", c

    print("Optimization Finished!")

    test_result = sess.run(pred, feed_dict={X: train_X})
    correct_pred = tf.equal(tf.argmax(test_result, 1), tf.argmax(train_Y, 1))

    accuracy = tf.reduce_mean(tf.cast(correct_pred, "float"))

    y_p = tf.argmax(pred, 1)
    val_accuracy, y_pred = sess.run([accuracy, y_p], feed_dict={X: train_X, Y: train_Y})

    print "Accuracy:", val_accuracy
    y_true = np.argmax(train_Y, 1)
    print "Precision", precision_score(y_true, y_pred)
    print "Recall", recall_score(y_true, y_pred)
    print "f1_score", f1_score(y_true, y_pred)

end_time = time.time()

print "Completed in ", end_time - start_time, " seconds"