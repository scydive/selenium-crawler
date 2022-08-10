from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import networkx as nx
import matplotlib.pyplot as plt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import random

#PATH should be set to wherever your chromedriver installation is.
#Chromedriver downloads can be found at https://chromedriver.chromium.org/downloads.
#Please make sure you download the correct driver for your version of chrome.
PATH = 'insert chromedriver location here'
op = Options()
op.add_argument('--headless')
driver = webdriver.Chrome(PATH)

#edges and nodes for graph construction
edges = []
nodes = []

def scrolldown():
    for i in range(5):
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(.4)

#Sleep functions ensure the websites are able to load properly
time.sleep(3)

#Establishes a list of possible hashtags to look at, as well as already visited hashtags
possible = []
visited = []
loops = 0

#This link is the initial hashtag that will be visited, the second hashtag is defined further down.
driver.get('https://twitter.com/search?q=%23malazan')

#This function finds all hashtags on a given twitter page and adds them to the list of possible hashtags to visit.
#Further iterations will draw from the list of possible hashtags to explore, adding them to the visited list as it goes on.
#function is non-optimal, consideration for improvement at later date to make it more lightweight, remove global variables etc.
def locate():
    timeout = 0
    temp_limit = []
    scrolldown()
    time.sleep(8)
    global visited
    global possible
    global loops
    while len(temp_limit) <= 20:
        scrolldown()
        time.sleep(6)
        more = driver.find_elements(By.XPATH, '//a[starts-with(@href, "/hashtag/")]')
        for x in more:
            link = x.get_attribute(('href'))
            hashtags = x.get_attribute(('text'))
            if hashtags not in visited:
                nodes.append(link)
                edges.append((link, driver.current_url))
                possible.append(link)
                visited.append(hashtags)
                temp_limit.append(hashtags)
            else:
                pass
        timeout +=1
        if timeout >= 6:
            print('Not enough hashtags found, moving on.')
            break


locate()

#This function makes sure the locate function runs an approriate number of times.
#Non-optimal, could be baked into the locate function with improvements.
def repeat():
    counter = 0
    for link in possible:
        global loops
        driver.get(link)
        try:
            locate()
        except:
            locate()
        counter +=1
        if counter >= 20:
            break

repeat()
driver.get('https://twitter.com/search?q=%23currentlyreading')
possible = []

locate()
repeat()

#Builds a graph based on the crawled hashtags.
#The graph should contain two separate primary nodes, 20 nodes from each of those nodes, then 20 nodes from each of those resulting nodes.
#for the best result one should select two hashtags that could intermingle.
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw(G, with_labels=True)
nx.write_graphml(G, 'name2.graphml')
plt.show()
driver.quit()
