######################################################################
# ArdavanBidgoli
# CMU School of Architecture
# Robotic Plastering Project
# Feedback-loop image classifier
# Tested with/for:
#   Tensorflow 0.12.1
#   OpenCV 3.2.0-dev
######################################################################
# this code has been inspired by:
# https://codelabs.developers.google.com/
#       codelabs/tensorflow-for-poets/index.html?index=
#       ../../index#4
######################################################################


# Imports
######################################################################

# Import Tensorflow
import tensorflow as tf

# Import libraries for:
# System read and write, Checking object types, Time keeping
import sys
import time
import os
from os import listdir
from os.path import isfile, join, exists
from shutil import copyfile

# import json for json formatting
import json

# General Setup
######################################################################
# print in-progress report
printSwitch = True
# Sets the naming standard
sampleFolder = "./tests"
# Set log file info
logFolder = "./log"
logFileName = "log"
# keep track of time
start_time = time.time()

# Error messages:
nameFinderError= "File names cannot be read"
fileReadError = "Couldn't read files"


# Report messages:
saveToFileReport = "Data saved to the file: "
# Functions
######################################################################

# Returns a list of samples files
# Helper Function
def nameFinder(folder):
    # filters only the .jpg files from the folder
    try:
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        imageNames = [f for f in files if f.split(".")[1] == "jpg"]
        return imageNames
    except:
        print (nameFinderError)

# Reads the sample files
def loadSamples(folder):
    sampleData = []
    # Loads files at ./tests folder to test based on the trained model 
    # only lists the .jpg files
    # collects all file names
    try:
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        # filters only the .jpg files
        images = [f for f in files if f.split(".")[1] == "jpg"]
        size = len(images)
        for img in images:
            newPath = folder+"/"+img
            newSample = tf.gfile.FastGFile(newPath, 'rb').read()
            sampleData.append(newSample)
        return sampleData
    except:
        print (fileReadError)

# Classifies the images
def classifier(sampleData, sampleNames):
    fails = dict()
    size = len(sampleData)
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("retrained_labels.txt")]
    # Unpersists graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        ####################################################
        # just a hacky way to solve version discrpancies
        # if using older versions of Tensorflow,
        # remove this line!
        del(graph_def.node[1].attr["dct_method"])
        ####################################################
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        # iterating over iamges
        for i in range (size):
        #for image_data_item in image_data:
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': sampleData[i]})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            human_string = label_lines[top_k[0]]
            score = predictions[0][top_k[0]]

            # print report during the process
            if (printSwitch):
                print ("smaple ID", str(i))
                print('%s (score = %.2f)' % (human_string, score))
                #print('Correct answer: %s' %(sampleNames[i][:4]))
                print("------------------------------------")
            if (human_string != "pass" or score < 0.5):
                fails[sampleNames[i]] = human_string
                
    return fails

# Prints a brief report at the end
def report():
    finish_time = time.time()
    ellapsed_time = finish_time - start_time
    average_time = ellapsed_time / float(len(samples))

    # Print the final report
    print ('Total time:', str(int(ellapsed_time)))
    print ('Average time:', str(average_time)) 
    print("------------------------------------")
    print ("Failed samples:")
    for fail in fails:
        print (fail,"\t",fails[fail])
    print("------------------------------------")

# Writes data to file
# Helper function
def saveToFile(folder, logName,fails):
    # converts fails to json format
    jsonData = json.dumps(fails)

    # check if the log directory exist
    if not exists(folder):
        os.makedirs(folder)
    # generates the file name to save the log
    date_string = time.strftime("_%H:%M")
    newName = logName+date_string+".txt"
    newPath = os.path.join (folder, newName)

    # writes to file
    log = open(newPath, "w")
    log.write(str(jsonData))
    log.close()
    print (saveToFileReport,newPath)

# Copies failed cases to log folder with class added to the name
def saveFailSamples(logFolder,sampleFolder,fails):
    for fail in fails:
        failedSamplePath = sampleFolder+"/"+fail
        name= fail.split(".")
        targetPath = logFolder+"/"+name[0]+"_"+fails[fail]+".jpg"
        copyfile(failedSamplePath, targetPath)
    
# Generates the log in log folder 
def logger(logFolder,logFileName,fails,sampleFolder):
    saveToFile(logFolder, logFileName, fails)
    saveFailSamples(logFolder, sampleFolder, fails)

# Main body of codes
######################################################################
# Main procedure
samples = loadSamples(sampleFolder)
sampleNames = nameFinder(sampleFolder)
fails = classifier(samples,sampleNames)

# Reporting
logger(logFolder,logFileName,fails,sampleFolder)
report()




