#!/usr/bin/env python
# coding: utf-8
# %%

# %%


from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import datetime
from datetime import date
import utils 


# %%
db = utils.import_database()
MONTH_REGEX = utils.import_month_regex_var()
icalscr = utils.import_ical_scraper()

# %%


url = 'https://www.cb8m.com/calendar/?ical=1'
#today = date.today()
#url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?shortcode=76d4496d&ical=1'
events_dict = icalscr.ical_scraper(url)


# %%


database = db.Database(108)


# %%


for event in events_dict.values():
    database.addRow(title = event['topic'], date = event['date'] , details = event['description'], time = event['time'])


# %%




