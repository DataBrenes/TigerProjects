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
sleep(10)

num_list = [['7346455056',"T-Mobile"],['8432599611',"T-Mobile"]]
# Sunday= ck.available(browser,'Sunday','magic')
Monday= ck.available(browser,'Monday','holly') 
# Sunday= ck.available(browser,'Sunday','magic')
#Monday2= ck.available(browser,'Monday','magic')

if Sunday:
    txt.send(num_list,Monday2.encode('utf-8'))
if Monday:
    txt.send(num_list,Monday.encode('utf-8'))
if Monday2:
    txt.send(num_list,Monday2.encode('utf-8'))

browser.close()
# if Sunday:
#     print(Sunday)
# if Monday:
#     print(Monday)

