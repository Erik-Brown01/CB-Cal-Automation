#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX
import datetime
from datetime import date
import lib.ical_scraper as icalscr


# In[2]:


url = 'https://cbbrooklyn.cityofnewyork.us/cb17/events/month/'
today = date.today()
url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?shortcode=588d7eac&ical=1'
events_dict = icalscr.ical_scraper(url)


# In[3]:


database = db.Database(317)


# In[4]:


for event in events_dict.values():
    database.addRow(title = event['topic'], date = event['date'] , details = event['description'], time = event['time'])


# In[ ]:




