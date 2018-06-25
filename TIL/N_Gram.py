# N-gram Model

import math, random, re
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import requests

def fix_unicode(text):
    return text.replace(u"\u2019","'")

def get_document():
    url = "https://www.oreilly.com/ideas/what-is-data-science"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    content = soup.find("div", "article-body")
    regex = r"[\w']+|[\.]"
    
    document = []
    
    for paragraph in content("p"):
        words = re.findall(regex, fix_unicode(paragraph.text))
        document.extend(words)
        
    return document

document = get_document()
bigrams = zip(document, document[1:])
transitions = defaultdict(list)
for prev, current in bigrams: transitions[prev].append(current)
    
def generate_using_bigrams(transitions):
    current = "."
    result = []
    while True:
        next_word_candidates = transitions[current]
        current = random.choice(next_word_candidates)
        result.append(current)
        if current == '.': return " ".join(result)
        
#generate_using_bigrams(transitions)

trigrams = zip(document, document[1:], document[2:])
trigram_transitions = defaultdict(list)
starts = []
for prev, current, next_ in trigrams:
    if prev == '.': starts.append(current)
    trigram_transitions[(prev, current)].append(next_)

def generate_using_trigrams(starts, trigram_transitions):
    current = random.choice(starts)
    prev = '.'
    result = [current]
    while True:
        next_word_candidates = trigram_transitions[(prev, current)]
        next_ = random.choice(next_word_candidates)
        
        prev, current = current, next_
        result.append(current)
        if current == '.': return " ".join(result)

#generate_using_trigrams(starts, trigram_transitions)
