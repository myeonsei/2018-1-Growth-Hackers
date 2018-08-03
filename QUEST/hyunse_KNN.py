import numpy as np; import pandas as pd; import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier; from os import listdir
from sklearn.model_selection import train_test_split

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
kk = list(range(1, 11)); corr = []
Y_train

for k in range(1, 11):
    classify = KNeighborsClassifier(n_neighbors=k)
    classify.fit(X_train, Y_train)
    Y_pred = classify.predict(X_test)
    corr.append(np.mean(Y_test == Y_pred))
    
plt.scatter(kk, corr); plt.legend(loc='best')
k = np.array(corr).argmax() + 1
classify = KNeighborsClassifier(n_neighbors=k)
classify.fit(X_train, Y_train)

# test data
datadir = 'C:\\Users\\myeon\\Desktop\\Data Science\\knn quest\\data\\testDigits'
test_data = read_num(datadir)
testX = test_data[:, :-1]; testY = test_data[:, -1]
test_pred = classify.predict(testX)
accu = np.mean(testY == test_pred)
