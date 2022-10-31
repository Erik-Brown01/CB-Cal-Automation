#!/usr/bin/env python
# coding: utf-8

# In[7]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX
import datetime
from datetime import date
import lib.ical_scraper as icalscr


# In[8]:


url = 'https://www.cb5.org/cb5m/calendar.ics'
#today = date.today()
#url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?shortcode=76d4496d&ical=1'
events_dict = icalscr.ical_scraper(url)


# In[9]:


database = db.Database(105)


# In[10]:


for event in events_dict.values():
    database.addRow(title = event['topic'], date = event['date'] , details = event['description'], time = event['time'])


# In[ ]:




