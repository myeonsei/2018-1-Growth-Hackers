# 데이터 예시 : ({'Outlook': 'sunny', 'Temperature': 'hot', 'Humidity': 'high', 'Windy': 'FALSE'}, False)

import math
from collections import Counter, defaultdict
from functools import partial

def entropy(class_probabilities):
    return sum(-p*math.log(p,2) for p in class_probabilities if p)

def class_probabilities(labels):
    total = len(labels)
    return [count/total for count in Counter(labels).values()]

def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    return entropy(class_probabilities(labels)) # 그냥 주어진 list의 entropy를 반환.

def partition_entropy(subsets): # subsets의 형태로 줬을 때 entropy 반환
    total = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset)*len(subset)/total for subset in subsets)

def partition_by(inputs, attribute):
    groups = defaultdict(list)
    for input_ in inputs:
        key = input_[0][attribute]
        groups[attribute].append(input_)
    return groups # attribute별로 input들 묶어서 반환해주는 것.

def partition_entropy_by(inputs, attribute):
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values()) # attribute 주어질 때 그걸 기준으로 엔트로피 계산 및 반환

def build_tree_id3(inputs, split_candidates = None):
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()
    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label]); num_falses = num_inputs - num_trues
    
    if num_trues == 0:
        return False
    if num_falses == 0:
        return True
    if not split_candidates:
        return num_trues >= num_falses
    
    best_attribute = min(split_candidates, key=partial(partition_entropy_by, inputs))
    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates if a != best_attribute]
    
    subtrees = {attribute: build_tree_id3(subset, new_candidates) for attribute, subset in partitions.items()}
    subtrees[None] = num_trues > num_falses
    
    return (best_attribute, subtrees)

def classify(tree, input_):
    if tree in [True, False]:
        return tree
    
    attribute, subtree_dict = tree
    subtree_key = input_.get(attribute)
    
    if subtree_key not in subtree_dict:
        subtree_key = None
    
    subtree = subtree_dict[subtree_key]
    
    return classify(subtree, input_)

## setting finished ##

inputs = [({'Outlook': 'sunny', 'Temperature': 'hot', 'Humidity': 'high', 'Windy': 'FALSE'}, False),({'Outlook': 'sunny', 'Temperature': 'hot', 'Humidity': 'high', 'Windy': 'TRUE'}, False),({'Outlook': 'overcast', 'Temperature': 'hot', 'Humidity': 'high', 'Windy': 'FALSE'}, True),({'Outlook': 'rain', 'Temperature': 'mild', 'Humidity': 'high', 'Windy': 'FALSE'}, True),({'Outlook': 'rain', 'Temperature': 'cool', 'Humidity': 'normal', 'Windy': 'FALSE'}, True),({'Outlook': 'rain', 'Temperature': 'cool', 'Humidity': 'normal', 'Windy': 'TRUE'}, False),({'Outlook': 'overcast', 'Temperature': 'cool', 'Humidity': 'normal', 'Windy': 'TRUE'}, True),({'Outlook': 'sunny', 'Temperature': 'mild', 'Humidity': 'high', 'Windy': 'FALSE'}, False),({'Outlook': 'sunny', 'Temperature': 'cool', 'Humidity': 'normal', 'Windy': 'FALSE'}, True),({'Outlook': 'rain', 'Temperature': 'mild', 'Humidity': 'normal', 'Windy': 'FALSE'}, True),({'Outlook': 'sunny', 'Temperature': 'mild', 'Humidity': 'normal', 'Windy': 'TRUE'}, True),({'Outlook': 'overcast', 'Temperature': 'mild', 'Humidity': 'high', 'Windy': 'TRUE'}, True),({'Outlook': 'overcast', 'Temperature': 'hot', 'Humidity': 'normal', 'Windy': 'FALSE'}, True),({'Outlook': 'rain', 'Temperature': 'mild', 'Humidity': 'high', 'Windy': 'TRUE'}, False)]

tree = build_tree_id3(inputs)
print(tree)
print(classify(tree, {'Outlook': 'sunny', 'Temperature': 'mild', 'Humidity': 'high', 'Windy': 'TRUE'}))
