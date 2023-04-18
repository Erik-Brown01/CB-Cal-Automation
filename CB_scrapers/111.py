#!/usr/bin/env python
# coding: utf-8
# %%

# %%


import unicodedata
import requests
import re
import datetime
from datetime import date
import pandas as pd
from datetime import datetime
import utils


# %%
db = utils.import_database()
MONTH_REGEX = utils.import_month_regex_var()
air_s = utils.import_airtable_scraper()

url = "https://airtable.com/embed/shrEZxc5vi8McZNFb/tblNt0o4xr7gTHHoY"
df = air_s.airtable_scraper(url)


# %%


df[['date', 'time']] = df['Date & Time'].str.split(' ', expand=True)
df['description'] = df.apply(lambda row: " \n ".join(["{}: {}".format(col, row[col]) for col in ['Register to Attend', 'Agenda', 'Minutes', 'Recording', 'Presentations'] if not pd.isna(row[col]) and row[col] != '']), axis=1)
df = df.drop(columns=['Date & Time', 'Register to Attend', 'Minutes', 'Recording', 'Presentations', 'Agenda'])
events_dict = {}
df.columns = [col.lower() for col in df.columns]
df = df.rename(columns = {"name": "topic"})
df['date'] = df['date'].apply(lambda x: datetime.strptime(x, "%m/%d/%Y").strftime("%m/%d/%y"))
df['time'] = df['time'].apply(lambda x: datetime.strptime(x, "%I:%M%p").strftime("%I:%M %p"))
events_list = df.to_dict('records')


# %%


database = db.Database(111)


# %%


#database.deleteDistrictEvents()
database.addListOfEvents(events_list)


# %%




