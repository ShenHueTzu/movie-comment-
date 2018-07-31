
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import lxml

res = requests.get('https://movies.yahoo.com.tw/movieinfo_review.html/id=8102?sort=update_ts&order=desc&page=1')
soup = BeautifulSoup(res.text,"lxml")

title_inChinese = soup.find("h1",{"class":"inform_title"}).text
title_inEng = soup.find("div",{"class":"inform_title_en"}).text


# In[3]:


from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

comment_total=[]

browser = webdriver.Chrome()
browser.get('https://movies.yahoo.com.tw/movieinfo_review.html/id=8102?sort=update_ts&order=desc&page=1')

#page1to3

for i in range(0,12):
    
    time.sleep(20)
    soup = BeautifulSoup(browser.page_source,"lxml")
    
    comment = [tag.text for tag in soup.select('.form_good span')]
    comment = [el.replace('\n', '') for el in comment]
    comment = [y for y in comment if y.strip()]
    
    comment_total.extend(comment)
    
    browser.find_element_by_css_selector('li.nexttxt > a').click()

browser.close()     


# In[4]:


r=re.compile(" [0-9]|[0-9]")
B= list(filter(r.match, comment_total))
comment_total_new= [x for x in comment_total if x not in B]


# In[14]:


mytext = ''.join(comment_total_new)


# In[20]:


import jieba 
mytext = " ".join(jieba.cut(mytext))


# In[25]:


from wordcloud import WordCloud 
wordcloud = WordCloud(font_path="simsun.ttf").generate(mytext)

import matplotlib.pyplot as plt 
plt.imshow(wordcloud, interpolation='bilinear') 
plt.axis("off")

