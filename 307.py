#!/usr/bin/env python
# coding: utf-8

# In[19]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import database as db


# In[2]:


url = 'https://www1.nyc.gov/site/brooklyncb7/calendar/calendar.page'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
body = soup.find(class_='about-description').find_all(True, recursive=False)


# In[3]:


blocks = []
block = []

for tag in body:
    #find start of event with every h3 tag and append it to blocks
    if tag.name == 'h3':
        if len(block) == 0:
            block.append(tag)
        else:
            blocks.append(block)
            #block.append(tag)
            block = []
            block.append(tag)
    #if h3 tag not found append the tag to previous block
    elif tag.name != 'h2':
        block.append(tag)


# In[11]:


events_dict = {}
for i,block in enumerate(blocks):
    #test if block has h3 tag
    flag = [True for line in block if line.name == 'h3']

    if not flag: continue
    
    title = None
    date = None
    time = None
    details = None
    
    for line in block:
        if line.name == 'h3' and title == None: 
            title = line.text
        if line.name == 'p' and date == None and time == None:
            date = re.search(r'<p>(.+\d)<br\/>', str(line))
            time = re.search('<br\/>(.+)<br\/>', str(line))
            if date is not None and time is not None:
                date = date.group(1)
                time = time.group(1)
        elif date is not None and time is not None:
            if details is None:
                details = line.text
             
            else:
                details = details + "\n" + line.text
                
    events_dict[i] = {
    'date': date,
    'time':time,
    'title': title,
    'details':details
    }
                
    print(events_dict)
    #print (f"Title: {title} \nDate: {date}\nTime: {time}\nDetails:{details}\n-----------------------\n")
    
#         date = where tag == 'p'
#         time = where tag == 'br'
#         title = where tag == 'h3'
#         details = 
    


# In[20]:


database = db.Database(307)

for event in events_dict.values():
    database.addRow(title = event['title'], date = event['date'] , details = event['details'], time = event['time'])

