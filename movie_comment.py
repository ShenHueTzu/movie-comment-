
# coding: utf-8



import requests
from bs4 import BeautifulSoup
import lxml

#get data from Yahoo movie with 柯南

res = requests.get('https://movies.yahoo.com.tw/movieinfo_review.html/id=8102?sort=update_ts&order=desc&page=1')
soup = BeautifulSoup(res.text,"lxml")

title_inChinese = soup.find("h1",{"class":"inform_title"}).text
title_inEng = soup.find("div",{"class":"inform_title_en"}).text

#use selenium automatically manipulate webdriver(Chorme)

from selenium import webdriver
import time
import re

comment_total=[]

browser = webdriver.Chrome()
browser.get('https://movies.yahoo.com.tw/movieinfo_review.html/id=8102?sort=update_ts&order=desc&page=1')


for i in range(0,12):
    
    time.sleep(20) #avoid detecting 
    soup = BeautifulSoup(browser.page_source,"lxml")
    
    
    comment = [tag.text for tag in soup.select('.form_good span')]
    comment = [el.replace('\n', '') for el in comment]
    comment = [y for y in comment if y.strip()]
    
    comment_total.extend(comment)
    
    #自動跳頁
    browser.find_element_by_css_selector('li.nexttxt > a').click()

browser.close()     


#過濾文字
r=re.compile(" [0-9]|[0-9]")
B= list(filter(r.match, comment_total))
comment_total_new= [x for x in comment_total if x not in B]

#convert list to a string
mytext = ''.join(comment_total_new)


#分詞
import jieba 
mytext = " ".join(jieba.cut(mytext))


#
from wordcloud import WordCloud 
wordcloud = WordCloud(font_path="simsun.ttf").generate(mytext)

import matplotlib.pyplot as plt 
plt.imshow(wordcloud, interpolation='bilinear') 
plt.axis("off")

