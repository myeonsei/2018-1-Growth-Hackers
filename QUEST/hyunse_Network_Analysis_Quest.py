from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pickle

import time

driver = webdriver.Chrome("C:\\Users\\myeon\\Desktop\\Data Science\\ds_1st_session\\Utility\\chromedriver.exe")
driver.get("https://search.naver.com/search.naver?where=news&query=%EB%AC%B8%EC%9E%AC%EC%9D%B8%20%ED%91%B8%ED%8B%B4&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=&mynews=1&mson=0&refresh_start=0&related=0")
driver.find_element_by_css_selector('#_search_option_btn > span').click()
driver.find_element_by_css_selector('#news_popup > a').click()
driver.find_element_by_css_selector('#ca_p1').click()
driver.find_element_by_css_selector('#_nx_option_media > div.con_bx > div.view_btn > button.impact._submit_btn').click()
driver.implicitly_wait(1)
#driver.maximize_window()

wait = WebDriverWait(driver, 100)

headlines = []; press = []


for i in range(30):
    for j in range(10):
        try:
            headline = driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/ul/li[{}]/dl/dt/a'.format(j+1)).text
            news = driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/ul/li[{}]/dl/dd/span'.format(j+1)).text
            headlines.append(headline)
            press.append(news)
        except:
            print("에러발생")

    print(i)
    driver.find_element_by_css_selector('#main_pack > div.paging > a.next').click()
    time.sleep(2)

print(headlines)
print(news)

with open("c:\\Users\\myeon\\Desktop\\network_text_문재인.txt", "wb") as f:
    pickle.dump(headlines, f)
    
with open("c:\\Users\\myeon\\Desktop\\network_text_문재인뉴스.txt", "wb") as f:
    pickle.dump(press, f)    

############

import networkx as nx
import matplotlib.pyplot as plt
from konlpy.tag import Twitter
from konlpy.corpus import kobill
import pickle
from collections import defaultdict
import numpy as np
from collections import Counter

def generate_edges(headline, news):
    test = []
    for i in range(len(headline)):
        test.append((headline[i], news))
    return test

with open("c:\\Users\\myeon\\Desktop\\network_text_문재인.txt", "rb") as f:
    headlines = pickle.load(f)
    
with open("c:\\Users\\myeon\\Desktop\\network_text_문재인뉴스.txt", "rb") as f:
    press = pickle.load(f)
    
press = list(map(lambda x: x.replace('언론사 선정', ''), press)) 

t = Twitter()

node_dic = defaultdict(int)
edges = []

for headline, news in zip(headlines, press):
    tags_ko = t.pos(headline)
    temp = []

    for word, pumsa in tags_ko:
        # print(word, pumsa)
        # if len(word) > 1 and (pumsa == 'Noun' or pumsa == 'Verb' or pumsa == 'Adjective'):
        # if len(word) > 1 and (pumsa == 'Noun' or pumsa == 'Verb'):
        if len(word) > 1 and (pumsa == 'Noun'):
            node_dic[word] += 1
            temp.append(word)

    edges.extend(generate_edges(temp, news))

sorted_nodes = sorted(node_dic, key=node_dic.get, reverse=True)
press_count = defaultdict(int)
for i in press:
    press_count[i] += 1
sorted_press = sorted(press_count, key=press_count.get, reverse=True)
#sorted_press = sorted(press, key=press.Counter(), reverse=True)
# nodes = list(set(nodes))
nodes = sorted_nodes[2:20]#; nodes.extend(list(set(press)))
l = len(nodes)
edges = list(set(edges))
nodes.extend(sorted_press[:5])

remove = []
for i, (word1, word2) in enumerate(edges):
    if word1 not in nodes:
        remove.append((word1, word2))
    elif word2 not in nodes:
        remove.append((word1, word2))

for _tuple in remove:
    edges.remove(_tuple)

# print(len(nodes))
# print(len(edges))

# print(nodes)
# print(edges)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
pos = nx.spring_layout(G)

d = nx.degree(G)

print(pos)
print(d)

lst = [b for a,b in d]
temp = np.asarray(lst)
temp1 = temp[:l]; temp2 = temp[l:]
print(temp)

#nx.draw_spring(G, node_size = temp*10, font_size=20)
nx.draw_networkx_nodes(G, pos, nodelist=nodes[:l], node_size = temp1*30, node_color='blue')
nx.draw_networkx_nodes(G, pos, nodelist=nodes[l:], node_size = temp2*30, node_color='red')
nx.draw_networkx_edges(G, pos, width=.5, alpha=.5, edge_color='k')
nx.draw_networkx_labels(G, pos, font_family='Malgun Gothic')

betweenness_cen = nx.betweenness_centrality(G)
closeness_cen = nx.closeness_centrality(G)

# print(betweenness_cen)
# print(closeness_cen)

plt.show()
