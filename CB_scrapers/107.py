#!/usr/bin/env python
# coding: utf-8
# %%

# %%

import utils
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import re
import calendar
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
db = utils.import_database()
date_regex = utils.import_date_regex_var()
time_regex = utils.import_time_regex_var()


# %%


url = 'https://www.nyc.gov/site/manhattancb7/meetings/full-board-agenda.page'
#convert the webpage to soup
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#find the webpage body with event details
body = soup.find(class_='span6 about-description')

blocks = []
block = []
for tag in body:
    #find start of event with every h3 tag and append it to blocks
    if tag.name == 'h1':
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
    flag = [True for line in block if line.name == 'h1']

    if not flag: continue
    
    topic = None
    date = None
    time = None
    description = None
    
    for line in block:
        if line.name == 'h1' and topic == None: 
            topic = line.text
        if line.name == 'p' and date == None and time == None:
            #print(str(line) + '\n')
            date = re.search(date_regex, str(line))
            time = re.search(time_regex, str(line))
            #print(time)
            #if date is not None and time is not None:
            if date is not None:
                #print(date.group(1))
                date_obj = datetime.strptime(date.group() + " " + str(datetime.now().year), "%A, %B %d %Y")
                date = date_obj.strftime("%m/%d/%y")
            if time is not None:
                time_obj  = datetime.strptime(time.group(), "%I:%M %p")
                time = time_obj.strftime("%I:%M %p")
        if description is None:
            description = line.text
        else:
            description = str(description + '\n' + line.text)
                
    events_dict[len(events_dict)] = {
    'date': date,
    'time':time,
    'topic': topic,
    'description':description
    }


# %%


database = db.Database(107)


# %%
database.addDictionary(events_dict)


# %%




