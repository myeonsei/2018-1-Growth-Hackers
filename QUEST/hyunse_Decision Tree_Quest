import numpy as np; import pandas as pd; from sklearn.datasets import load_breast_cancer; from sklearn.model_selection import train_test_split; from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier; from sklearn.ensemble import RandomForestClassifier

cancer = load_breast_cancer()
feature_names = cancer['feature_names']; features = cancer['data']; label_names = cancer['target_names']; labels = cancer['target']
train, test, train_labels, test_labels = train_test_split(features, labels, test_size = 0.33, random_state = 42)

decision_tree = DecisionTreeClassifier(max_depth=2, random_state=42).fit(train, train_labels)
random_forest = RandomForestClassifier(max_depth=2, random_state=42).fit(train, train_labels)

def measure_performance(X, y, clf):
    y_pred = clf.predict(X)
    print(str(clf)[:22])
    print('Accuracy: ', metrics.accuracy_score(y, y_pred), '\n')
    print('Classification report')
    print(metrics.classification_report(y, y_pred), '\n')
    print('Confusion report')
    print(metrics.confusion_matrix(y, y_pred), '\n')
    
measure_performance(train, train_labels, decision_tree); measure_performance(train, train_labels, random_forest)

####### RESULTS BELOW #######
# DecisionTreeClassifier
# Accuracy:  0.9448818897637795 

# Classification report
#              precision    recall  f1-score   support

#           0       0.90      0.96      0.93       145
#           1       0.97      0.94      0.95       236

# avg / total       0.95      0.94      0.95       381
 

# Confusion report
# [[139   6]
#  [ 15 221]] 

# RandomForestClassifier
# Accuracy:  0.952755905511811 

# Classification report
#              precision    recall  f1-score   support

#           0       0.97      0.90      0.94       145
#           1       0.94      0.98      0.96       236

# avg / total       0.95      0.95      0.95       381
 

# Confusion report
# [[131  14]
#  [  4 232]] 
