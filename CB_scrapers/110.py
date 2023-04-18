#!/usr/bin/env python
# coding: utf-8
# %%

# %%


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import utils
import datetime
from datetime import date


# %%
db = utils.import_database()
MONTH_REGEX = utils.import_month_regex_var()
icalscr = utils.import_ical_scraper()

# %%


url = 'https://cbmanhattan.cityofnewyork.us/cb10/events/month/'
today = date.today()
url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?ical=1'
events_dict = icalscr.ical_scraper(url)


# %%


database = db.Database(110)


# %%


for event in events_dict.values():
    database.addRow(title = event['topic'], date = event['date'] , details = event['description'], time = event['time'])


# %%




