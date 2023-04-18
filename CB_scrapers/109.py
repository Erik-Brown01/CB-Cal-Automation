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


url = 'https://calendar.google.com/calendar/ical/g4b54u7hbpp1b6p63gp0n97448@group.calendar.google.com/public/basic.ics'
events_dict = icalscr.ical_scraper(url)


# %%


database = db.Database(109)


# %%


database.deleteDistrictEvents()
database.addDictionary(events_dict)


# %%




