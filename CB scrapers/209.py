#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import re
import calendar
from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import lib.database as db
from lib.reconst import date_regex
from lib.reconst import time_regex


# In[3]:


url = 'https://www.nyc.gov/site/bronxcb9/calendar/calendar.page'
#convert the webpage to soup
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#find the webpage body with event details
body = soup.find(class_='span6 about-description')

blocks = []
block = []
for tag in body:
    #find start of event with every h3 tag and append it to blocks
    if tag.name == 'h2':
        if len(block) == 0:
            block.append(tag)
        else:
            blocks.append(block)
            #block.append(tag)
            block = []
            block.append(tag)
    #if h3 tag not found append the tag to previous block
    else:
        block.append(tag)

blocks.append(block)
blocks
        
events = []
event = {
    'title': None,
    'date': None,
    'details': ''
}

events_dict = {}
for i,block in enumerate(blocks):
    #test if block has h3 tag
    flag = [True for line in block if line.name == 'h2']

    if not flag: continue
    
    topic = None
    date = None
    time = None
    description = None
    
    for line in block:
        if line.name == 'h3' and topic == None: 
            topic = line.text
        if line.name == 'h2' and date == None and time == None:
            #print(str(line) + '\n')
            date = re.search(date_regex, str(line))
            time = re.search(time_regex, str(line))
            #print(time)
            #if date is not None and time is not None:
            if date is not None:
                #print(date.group(1))
                date = date.group()
            if time is not None:
                time = time.group()
        if description is None:
            description = line.text
        else:
            description = str(description + '\n' + line.text)
                
    events_dict[i] = {
    'date': date,
    'time':time,
    'topic': topic,
    'description':description
    }


# In[19]:


database = db.Database(209)


# In[20]:


database.deleteDistrictEvents()
database.addDictionary(events_dict)


# In[ ]:




