#!/usr/bin/env python
# coding: utf-8

# In[6]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX
import datetime
from datetime import date
import lib.ical_scraper as icalscr


# In[7]:


url = 'https://cbmanhattan.cityofnewyork.us/cb4/events/month/'
today = date.today()
url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?shortcode=76d4496d&ical=1'
events_dict = icalscr.ical_scraper(url)


# In[8]:


database = db.Database(104)


# In[9]:


for event in events_dict.values():
    database.addRow(title = event['topic'], date = event['date'] , details = event['description'], time = event['time'])


# In[ ]:




