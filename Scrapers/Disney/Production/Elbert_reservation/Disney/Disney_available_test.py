#!/usr/bin/env python
# coding: utf-8

# In[10]:


from providers import PROVIDERS
import check_available as ck
from time import sleep
from selenium import webdriver
import send_text as txt
# from importlib import reload
# reload(ck)

# instatiate browser and open page
browser = webdriver.Chrome()
URL = 'https://disneyworld.disney.go.com/availability-calendar/?segments=tickets,resort,passholder&defaultSegment=tickets'
browser.get(URL)
sleep(20)

num_list = [['7346455056',"T-Mobile"],['7346455056',"T-Mobile"]]
Sunday= ck.available(browser,'Sunday','epcot')
Monday= ck.available(browser,'Monday','epcot') 

if Sunday:
    txt.send(num_list,Sunday.encode('utf-8'))
if Monday:
    txt.send(num_list,Monday.encode('utf-8'))

browser.close()
# if Sunday:
#     print(Sunday)
# if Monday:
#     print(Monday)

