#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import database as db
month_regex = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\s\d+'


# In[4]:


url = 'https://linktr.ee/BKCB6Calendar'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
buttons = soup.find(class_='sc-bdfBwQ jrDHLp').find_all(True, recursive=False)


# In[5]:


t1 = buttons[0].find(class_='sc-iktFzd gaGeRK')
#buttons[0]
#t1
a_tag = t1.find('a', href=True) 
print(a_tag['href']) 


# In[6]:


a_tag = t1.find('a', href=True) 
print(a_tag['href']) 


# In[7]:


text = t1.find(class_='sc-hKgILt sc-iUuytg gXKGT esdhrP').text
title = re.search('\d+\s(.+)', text).group(1)
title


# In[8]:


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
    #time = None
    details = None
    
    t1 = button.find(class_='sc-iktFzd gaGeRK')
    
    if title == None and date == None:
        text = t1.find(class_='sc-hKgILt sc-iUuytg gXKGT esdhrP').text
        date = re.search(month_regex, text).group()
        title = re.search('\d+\s(.+)', text).group(1)
     
    url = str(t1.find('a', href=True)['href'])
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    text_content_cells = soup.find_all(class_="text_content-cell content-padding-horizontal")
    for text_box in text_content_cells:
        if details is None:
                details = text_box.text
             
        else:
            details = details + "\n" + text_box.text
    
    events_dict[i] = {
        'date': date,
        #'time':time,
        'title': title,
        'details':details
    }
    
    print (f"Title: {title} \nDate: {date}\nDetails:{details}\n-----------------------\n")
    
    
    
  


# In[9]:


url = str(t1.find('a', href=True)['href'])
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
text = str(soup.find(class_="text_content-cell content-padding-horizontal").text)
text = print(text)
#text


# In[3]:


database = db.Database(306)


# In[17]:


for event in events_dict.values():
    database.addRow(title = event['title'], date = event['date'] , details = event['details'], time = 'N/A')


# In[ ]:




