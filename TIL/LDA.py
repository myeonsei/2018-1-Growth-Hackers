from __future__ import division
import math, random, re 
from collections import defaultdict, Counter 
from bs4 import BeautifulSoup 
import requests 

documents = [["Support",  "Strange", "Unusual",  "fantasy",  "conspiracy"],
["Nano", "Art,", "Reloaded"],
["MUTEK" , "VIRTUAL", "FESTIVAL" ,"STUDIO", "project"],
["SketchPad", "Pro", "Filmmaker","Storyboard",  "iPad"],
["APPLES", "LEMONS", "REVIEWS"],
["HEART", "ART",  "PORTRAIT", "DESIGN", "COLLECTION"],
["From","Snapshot" , "Art"],
["Local", "Autonomy" ,"Networks", "Find", "Each" ,"Other"],
["Morning", "Sketch", "Calendar"],
["Apathetic", "Fairy", "Tales", "Magical", "Stories","Sub-par","Delivery"]]

K = 4

document_topic_counts = [Counter() for _ in documents]
topic_word_counts = [Counter() for _ in range(K)] 
topic_counts = [0 for _ in range(K)] 
document_lengths = [len(d) for d in documents]
distinct_words = set(word for document in documents for word in document) 
W = len(distinct_words)
D = len(documents)

random.seed(0)
document_topics = [[random.randrange(K) for word in document]
                   for document in documents]

for d in range(D):
    for word, topic in zip(documents[d], document_topics[d]):
        document_topic_counts[d][topic] += 1
        topic_word_counts[topic][word] += 1
        topic_counts[topic] += 1

def p_topic_given_document(topic, d, alpha=0.1): 
    return ((document_topic_counts[d][topic] + alpha) / (document_lengths[d] + K * alpha)) 
 
def p_word_given_topic(word, topic, beta=0.1):  
    return ((topic_word_counts[topic][word] + beta) / (topic_counts[topic] + W * beta)) 

def sample_from(weights): # weight에 맞게 index 뽑아내는.
     total = sum(weights)
     rnd = total * random.random()      
     for i, w in enumerate(weights):
         rnd -= w                    
         if rnd <= 0: return i          

def topic_weight(d, word, k): 
    return p_word_given_topic(word, k) * p_topic_given_document(k, d) 

def choose_new_topic(d, word): 
    return sample_from([topic_weight(d, word, k) for k in range(K)]) 

for iter in range(1000):
    for d in range(D): 
        for i, (word, topic) in enumerate(zip(documents[d], document_topics[d])): 
            document_topic_counts[d][topic] -= 1 
            topic_word_counts[topic][word] -= 1 
            topic_counts[topic] -= 1 
            document_lengths[d] -= 1 
 
            new_topic = choose_new_topic(d, word) 
            document_topics[d][i] = new_topic 

            document_topic_counts[d][new_topic] += 1 
            topic_word_counts[new_topic][word] += 1 
            topic_counts[new_topic] += 1 
            document_lengths[d] += 1

for k, word_counts in enumerate(topic_word_counts): 
         for word, count in word_counts.most_common(): 
             if count > 0: print (k, word, count) 

topic_names = ["A", "B", "C", "D"]

for document, topic_counts in zip(documents, document_topic_counts): 
         print (document) 
         for topic, count in topic_counts.most_common(): 
             if count > 0: 
                 print (topic_names[topic], count)
