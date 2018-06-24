import numpy as np; from matplotlib import pyplot as plt; import pandas as pd; import scipy.special; from os import listdir
from sklearn.neural_network import MLPClassifier; from sklearn.model_selection import train_test_split

def read_num(datadir): 
    training_file_list = listdir(datadir)
    data = np.zeros((len(training_file_list), 1025))

    for i in range(len(training_file_list)):
        tmp = open(datadir + '\\' + training_file_list[i]).readlines()
        for j in range(len(tmp)):
            tmp[j] = list(tmp[j].strip())
        data[i,:-1] = np.array(tmp).reshape(1024)
        data[i,-1] = training_file_list[i][0]
        
    return data

datadir = 'C:\\Users\\myeon\\Desktop\\Data Science\\knn quest\\data\\trainingDigits'
data = read_num(datadir).astype(np.int32)

dataX = data[:, :-1]
dataY = data[:, -1]
X_train, X_test, Y_train, Y_test = train_test_split(dataX, dataY, test_size=0.3, random_state=0)

mlp = MLPClassifier(solver='sgd', learning_rate_init=0.1, alpha=0, activation='logistic', random_state=10, max_iter=2000, hidden_layer_sizes=200, momentum=0)
mlp.fit(X_train, Y_train)
print(mlp.score(X_test, Y_test))
