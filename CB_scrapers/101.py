#!/usr/bin/env python
# coding: utf-8
# %%

# %%
import pandas as pd
import re
import utils as utils
from datetime import datetime


# %%


db = utils.import_database()
TIME_REGEX = utils.import_time_regex_var()
pdf_s = utils.import_pdf_scraper()


# %%


url = 'https://www.nyc.gov/site/manhattancb1/meetings/committee-agendas.page'


# %%


df, month, year = pdf_s.pdf_scraper(url)


# %%


eventArray = []
for i, column in df.items():
    for j, cell in enumerate(column):
        if j == 0:
            continue
        string_cell = str(cell)
        if not string_cell.isdigit() and not pd.isnull(cell):
            eventArray.append(string_cell)


# %%


eventArray = list(set(eventArray))
eventArray = [s for s in eventArray if s.split(' ')[0].isdigit() and int(s.split(' ')[0]) < 30]
eventArray = [
    re.sub('\s{2,}', ' ', re.sub('\\r', ' ', test_str))
    for test_str in eventArray
]
# eventArray1 = [re.split(r'_{2,}', entry) for entry in eventArray]
# eventArray1
def get_first_number(s):
    first_number = re.search(r'\d+', s)
    return first_number.group() if first_number else None

# Split entries with consecutive underscores and prepend the first number of the original entry
split_entries = []
for entry in eventArray:
    first_number = get_first_number(entry)
    new_entries = re.split(r'_{2,}', entry)
    if len(new_entries) > 1:
        numbered_new_entries = [new_entries[0]] + [f"{first_number} {e.strip()}" for e in new_entries[1:]]
    else:
        numbered_new_entries = new_entries
    split_entries.append(numbered_new_entries)

# Flatten the list of lists
flat_entries = [entry for sublist in split_entries for entry in sublist]


# %%


months_entries = [month + " " + entry for entry in flat_entries]


# %%


events = []
for entry in flat_entries:
    event = {}
    date_str = month + " " + str(re.match("\d+",entry).group(0)) + " " + str(year)
    event['date'] = datetime.strptime(date_str, "%B %d %Y").strftime("%m/%d/%y")
    event['time'] = re.search(TIME_REGEX, entry).group(0)
    event['topic'] = re.search(TIME_REGEX+'(?P<last_group>.*)', entry).group('last_group').strip()
    event['description'] = ""
    events.append(event)


# %%


database = db.Database(101)


# %%


database.addListOfEvents(events)


# %%




