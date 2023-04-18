#!/usr/bin/env python
# coding: utf-8

# In[31]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX


# In[32]:


url = 'https://linktr.ee/BKCB6Calendar'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
buttons = soup.find(class_='sc-bdfBwQ jrDHLp').find_all(True, recursive=False)


# In[33]:


# events_dict[i] = {
#     'date': date,
#     'time':time,
#     'title': title,
#     'details':details
#     }

events_dict = {}

for i,button in enumerate(buttons):
    title = None
    date = None
    time = None
    details = None
    
    t1 = button.find(class_='sc-iktFzd gaGeRK')
    
    if title == None and date == None:
        text = t1.find(class_='sc-hKgILt sc-iUuytg gXKGT esdhrP').text
        date = re.search(MONTH_REGEX, text).group()
        title = re.search('\d+(\w+)?\s(.+)', text).group(2)
     
    url = str(t1.find('a', href=True)['href'])
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    text_content_cells = soup.find_all(class_="text_content-cell content-padding-horizontal")
    for i,text_box in enumerate(text_content_cells):
        if details is None:
                details = text_box.text
             
        else:
            details = details + "\n" + text_box.text
        
        if re.search('((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp].[Mm].))',text_box.text) and time is None:
            time = re.search('((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp].[Mm].))',text_box.text).group()
            
    if time is None:
        time = 'N/A'
    
    events_dict[i] = {
        'date': date,
        'time':time,
        'title': title,
        'details':details
    }
    
    #print (f"Title: {title} \nDate: {date} \nTime:{time} \nDetails:{details}\n-----------------------\n")
    
    


database = db.Database(306)


# In[35]:


for event in events_dict.values():
    database.addRow(title = event['title'], date = event['date'] , details = event['details'], time = event['time'])


# In[ ]:




