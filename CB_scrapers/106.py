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


url = 'https://calendar.google.com/calendar/ical/cbsix.org_aln8v1ljifoiarn8ejne2mh81c@group.calendar.google.com/public/basic.ics'
events_dict = icalscr.ical_scraper(url)


# %%


database = db.Database(106)


# %%


database.deleteDistrictEvents()
database.addDictionary(events_dict)


# %%




