#!/usr/bin/env python
# coding: utf-8
# %%
from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import datetime
from datetime import date
import utils


# %%
icalscr = utils.import_ical_scraper()
db = utils.import_database()

# %%
url = 'https://cbmanhattan.cityofnewyork.us/cb2/events/month/'
today = date.today()
url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?ical=1'
events_dict = icalscr.ical_scraper(url)


# %%
database = db.Database(102)


# %%
database.addDictionary(events_dict)

# %%
