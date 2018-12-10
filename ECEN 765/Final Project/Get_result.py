# Fit data in model
from numpy import *
from os import listdir
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVR
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
import os,psutil
    
def img2vector(filename):
    returnVect = zeros((1,1890))
    fr = open(filename)
    for i in range(63):
        lineStr = fr.readline().split(' ')
        for j in range(30):
            returnVect[0,30*i+j] = int(lineStr[j])
    return returnVect

def error_rate(testLabels,result):
    m = len(testLabels)
    i = 0
    error = 0
    while i < m:
        if testLabels[i] != result[i] :
            error += 1
        i += 1
    rate = error/m
    return rate/2
def captchaClassTest():
    trainLabels = []
    trainingFileList = listdir('train')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1890))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = ord(fileStr.split('_')[0]) # Ascll for label
        trainLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('train/%s' % fileNameStr)
    print('Training data is set!')
    testLabels = []
    testFileList = listdir('test')        #iterate through the test set
    mTest = len(testFileList)
    testMat = zeros((mTest,1890))
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = ord(fileStr.split('_')[0])
        testLabels.append(classNumStr)
        testMat[i,:] = img2vector('test/%s' % fileNameStr)
    print('Test data is set!')
    info = psutil.virtual_memory()
    print( 'Used memory is ',psutil.Process(os.getpid()).memory_info().rss/1024/1024 ,'MB')
    # KNN
    neigh = KNeighborsClassifier(n_neighbors=5)
    neigh.fit(trainingMat,trainLabels)
    print('KNN is set!')
    result = neigh.predict(testMat)
    knn_rate=error_rate(testLabels,result)
    print('KNN error rate is %f' %knn_rate)
    info = psutil.virtual_memory()
    print( 'Used memory is ',psutil.Process(os.getpid()).memory_info().rss/1024/1024 ,'MB')

    #svm
    svm = SVR(gamma=1, C=1.0, epsilon=0.2)
    svm.fit(trainingMat,trainLabels)
    print('SVM is set!')
    result = svm.predict(testMat)
    svm_rate=error_rate(testLabels,result)
    print('SVM error rate is %f' %svm_rate)
    info = psutil.virtual_memory()
    print( 'Used memory is ',psutil.Process(os.getpid()).memory_info().rss/1024/1024 ,'MB')

    #MultinomialNB
    NB = MultinomialNB()
    NB.fit(trainingMat,trainLabels)
    print('NaiveBayes is set!')
    result = NB.predict(testMat)
    NB_rate=error_rate(testLabels,result)
    print('NaiveBayes error rate is %f' %NB_rate)
    info = psutil.virtual_memory()
    print( 'Used memory is ',psutil.Process(os.getpid()).memory_info().rss/1024/1024 ,'MB')

    #multi-layer perceptron(MLP)
    MLP = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    MLP.fit(trainingMat,trainLabels)
    print('MLP is set!')
    result = MLP.predict(testMat)
    MLP_rate=error_rate(testLabels,result)
    print('MLP error rate is %f' %MLP_rate)
    info = psutil.virtual_memory()
    print( 'Used memory is ',psutil.Process(os.getpid()).memory_info().rss/1024/1024 ,'MB')
captchaClassTest()
