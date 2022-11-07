#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX
import datetime
from datetime import date
import lib.airtable_scraper as air


# In[2]:


url = "https://airtable.com/embed/shrEZxc5vi8McZNFb/tblNt0o4xr7gTHHoY"
event_dict = air.airtable_scraper(url)


# In[4]:


database = db.Database(111)


# In[10]:


database.deleteDistrictEvents()
database.addDictionary(event_dict)


# In[ ]:




