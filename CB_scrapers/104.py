#!/usr/bin/env python
# coding: utf-8
# %%

# %%

import utils
from bs4 import BeautifulSoup
import unicodedata
import requests
import re
db = utils.import_database()
MONTH_REGEX = utils.import_month_regex_var()
import datetime
from datetime import date
icalscr = utils.import_ical_scraper()


# %%


url = 'https://cbmanhattan.cityofnewyork.us/cb4/events/month/'
today = date.today()
url = url + str(today.strftime("%Y")) + '-' + str(today.strftime("%m")) + '/' + '?shortcode=76d4496d&ical=1'
events_dict = icalscr.ical_scraper(url)


# %%


database = db.Database(104)


# %%
database.addDictionary(events_dict)

# %%




