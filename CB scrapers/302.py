#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX
import datetime
from datetime import date
import lib.ical_scraper as icalscr


# In[3]:


url = 'https://calendar.google.com/calendar/ical/bk02public@gmail.com/public/basic.ics'
events_dict = icalscr.ical_scraper(url)


# In[3]:


database = db.Database(302)


# In[4]:


database.deleteDistrictEvents()
database.addDictionary(events_dict)


# In[ ]:




