import numpy; from matplotlib import pyplot as plt; import pandas as pd; import scipy.special

#example = numpy.array(data.iloc[0,1:]).reshape((28,28))
#plt.imshow(example, cmap='Greys') # 시각화를 위한 부분

# 2-layer neural network hard coding started

class nn:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))
        
        self.lr = learningrate
        self.activation_function = lambda x: scipy.special.expit(x)
        
    def train(self, inputs_list, targets_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))
        
    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        return self.activation_function(numpy.dot(self.who, self.activation_function(numpy.dot(self.wih, inputs))))

input_nodes = 784; hidden_nodes = 200; output_nodes = 10; learning_rate = 0.1
n = nn(input_nodes, hidden_nodes, output_nodes, learning_rate)
data = pd.read_csv('C:\\Users\\myeon\\Desktop\\Data Science\\0529 신경망\\3rd_NN\\mnist_test.csv', header = None, dtype = int, engine = 'python')
data.iloc[:,1:] = data.iloc[:,1:]/255*0.99 + 0.01
output_nodes = 10

for i in range(len(data)):
    targets = numpy.zeros(output_nodes) + 0.01
    targets[data.iloc[i,0]] = 0.99
    n.train(data.iloc[i,1:], targets)

test_data = pd.read_csv('C:\\Users\\myeon\\Desktop\\Data Science\\0529 신경망\\3rd_NN\\mnist_train_100.csv', header = None, dtype = int, engine = 'python')
test_data.iloc[:,1:] = test_data.iloc[:,1:]/255*0.99 + 0.01
score = []

for i in range(len(test_data)):
    score.append(numpy.argmax(n.query(test_data.iloc[i,1:])) == test_data.iloc[i,0])

print(numpy.average(score))

# code using scikit-learn

from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(solver='sgd', learning_rate_init=0.1, alpha=0, batch_size=7000, activation='logistic', random_state=10, max_iter=2000, hidden_layer_sizes=200, momentum=0)
mlp.fit(data.iloc[:,1:], data.iloc[:,0])
mlp.score(test_data.iloc[:,1:], test_data.iloc[:,0])
