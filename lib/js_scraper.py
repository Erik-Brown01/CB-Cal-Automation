#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import urllib.request
from bs4 import BeautifulSoup 


# In[2]:


def isTime(testString):
    nowhitespace = testString.replace(" ", "")
    if re.search('((([0]?[1-9]|1[0-2])(:)([0-5][0-9]))(am|pm|PM|AM))', nowhitespace):
        return re.search('((([0]?[1-9]|1[0-2])(:)([0-5][0-9]))(am|pm|PM|AM))', nowhitespace)
    
    elif re.search('(\d(:\d\d)?(AM|PM|am|PM))-(\d(:\d\d)?(AM|PM|am|PM))', nowhitespace):
        return re.search('(\d(:\d\d)?(AM|PM|am|PM))-(\d(:\d\d)?(AM|PM|am|PM))', nowhitespace)
    
    else:
        return None


# In[3]:


# def js_scraper(url):
#     #print('\n\n ---', url)
#     file = urllib.request.urlopen(url)
#     text = file.read().decode('utf-8')

#     events = []
#     matches = re.findall('] = \"(.*)\"', text)
#     for match in matches:
#         #get all matches
#         date = ''
#         time = ''
#         title = ''
#         description = ''

#         date_re = re.search(r'(.*?)\|', match)
#         if date_re:
#             date = date_re.group(1)

#         after_date = match.split('|')[1]

#         soup = BeautifulSoup(after_date)
#         soup_text = soup.get_text(separator="\n")
#         soup_arr = soup_text.split('\n')

#         title = soup_arr[0]

#         soup_arr = list(dict.fromkeys(soup_arr))
#         for tag in soup_arr:
#             time_re = isTime(tag)
#             if time_re and time == '':
#                 time = time_re.group(1)

#             elif  time != '' and description == '':
#                 description = tag

#             elif time != '' and description != '':
#                 description=description + (' ') + str(tag)

#         if description == '':
#             description = " ".join(soup_arr[1:])

#         if soup.find('a', href=True):
#             link = soup.find('a', href=True).get("href")
#             if '"' in link:
#                 link = link.partition('"')[2]
#             if link[0]=='/':
#                 link = 'https://www.nyc.gov/' + link

#             link = re.sub(r"^\W+|\W+$", "", link)

#             description = description + ('\n') + 'Links:' + str(link)
            
#         #append event
#         events.append({
#             'date': date,
#             'time':time,
#             'topic': title,
#             'description':description
#         })
#     return events


# In[3]:


def js_scraper(url):
    print('\n\n ---', url)
    file = urllib.request.urlopen(url)
    text = file.read().decode('utf-8')

    events = []
    matches = re.findall('] = (\"|\')(.*)(\"|\')', text)
    for match in matches:
        match = match[1]
        #get all matches
        date = ''
        time = ''
        title = ''
        description = ''

        date_re = re.search(r'(.*?)\|', match)
        if date_re:
            date = date_re.group(1)

        after_date = match.split('|')[1]

        soup = BeautifulSoup(after_date)
        soup_text = soup.get_text(separator="\n")
        soup_arr = soup_text.split('\n')

        title = soup_arr[0]

        soup_arr = list(dict.fromkeys(soup_arr))
        for tag in soup_arr:
            time_re = isTime(tag)
            if time_re and time == '':
                time = time_re.group(1)

            elif  time != '' and description == '':
                description = tag

            elif time != '' and description != '':
                description=description + (' ') + str(tag)

        if description == '':
            description = " ".join(soup_arr[1:])
        links = soup.find_all('a', href=True)
        for link in links:
            link = link.get("href")
            if '"' in link:
                link = link.partition('"')[2]
            if link != '':
                if link[0]=='/':
                    link = 'https://www.nyc.gov/' + link
            link = re.sub(r"^\W+|\W+$", "", link)
            description = description + ('\n') + 'Link:' + str(link)
            
        #append event
        events.append({
            'date': date,
            'time':time,
            'topic': title,
            'description':description
        })
    return events




