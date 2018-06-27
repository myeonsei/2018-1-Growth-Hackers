from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pickle

import time

driver = webdriver.Chrome("C:\\Users\\myeon\\Desktop\\Data Science\\ds_1st_session\\Utility\\chromedriver.exe")
driver.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%AC%B8%EC%9E%AC%EC%9D%B8&oquery=%EA%B2%BD%EC%9A%B0%EC%9D%98+%EC%88%98&tqi=TzcX0lpySEhssb4CKWossssst58-193498")
driver.implicitly_wait(1)
#driver.maximize_window()

wait = WebDriverWait(driver, 100)

data = []


for i in range(10):
    for j in range(10):
        try:
            text = driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/ul/li[{}]/dl/dt/a'.format(j+1)).text
            print(text)
            data.append(text)
        except:
            print("에러발생")

    print(i)
    driver.find_element_by_css_selector('#main_pack > div.paging > a.next').click()
    time.sleep(2)

print(data)

with open("c:\\Users\\myeon\\Desktop\\network_text_월드컵.txt", "wb") as f:
    pickle.dump(data, f)

-----

import networkx as nx
import matplotlib.pyplot as plt
from konlpy.tag import Twitter
from konlpy.corpus import kobill
import pickle
from collections import defaultdict
import numpy as np

def generate_edges(nodes):
    test = []
    for i in range(len(nodes)):
        for j in range(len(nodes) - i):
            if j == 0:
                continue
            test.append((nodes[i], nodes[i + j]))
    return test

with open("c:\\Users\\myeon\\Desktop\\network_text_월드컵.txt", "rb") as f:
    data = pickle.load(f)

contents = data

t = Twitter()

node_dic = defaultdict(int)
edges = []

for text in contents:
    # 각각의 신문 기사 제목
    tags_ko = t.pos(text)
    temp = []

    for word, pumsa in tags_ko:
        # print(word, pumsa)
        # if len(word) > 1 and (pumsa == 'Noun' or pumsa == 'Verb' or pumsa == 'Adjective'):
        # if len(word) > 1 and (pumsa == 'Noun' or pumsa == 'Verb'):
        if len(word) > 1 and (pumsa == 'Noun'):
            node_dic[word] += 1
            temp.append(word)

    edges.extend(generate_edges(temp))

sorted_nodes = sorted(node_dic, key=node_dic.get, reverse=True)

# nodes = list(set(nodes))
nodes = list(set(sorted_nodes[2:20]))
edges = list(set(edges))

remove = []
for i, (word1, word2) in enumerate(edges):
    if word1 not in nodes:
        remove.append((word1, word2))
    elif word2 not in nodes:
        remove.append((word1, word2))

for _tuple in remove:
    edges.remove(_tuple)

print(len(nodes))
print(len(edges))

print(nodes)
print(edges)

G = nx.Graph()

G.add_nodes_from(nodes)
G.add_edges_from(edges)

pos = nx.shell_layout(G)

d = nx.degree(G)

print(pos)
print(d)

lst = [b for a,b in d]
temp = np.asarray(lst)

print(temp)

nx.draw_shell(G, node_size = temp*100, font_size=30)

nx.draw_networkx_labels(G, pos, font_family='Malgun Gothic')

betweenness_cen = nx.betweenness_centrality(G)
closeness_cen = nx.closeness_centrality(G)

# print(betweenness_cen)
# print(closeness_cen)

plt.show()
