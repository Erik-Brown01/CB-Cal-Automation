#!/usr/bin/env python
# coding: utf-8
# %%
from icalendar import Calendar, Event
from urllib.request import urlopen 
import urllib.request 
import requests
from bs4 import BeautifulSoup
import ssl   
from datetime import datetime
import re
from datetime import datetime


# %%


def ical_scraper(ical):
    context = ssl._create_unverified_context()
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    hdr={'User-Agent':user_agent,} 
    req=urllib.request.Request(ical,None,hdr)
    response = urllib.request.urlopen(req,context = context).read() 
    cal = Calendar.from_ical(response)
    events_dict = {}
    #iterrate through events in cal with new events from each 'vevent' 
    #add time,date, title and details to events_dict    
    for i, event in enumerate(cal.walk('vevent')):
        date = event.get('dtstart')
        try:
            time =  str(date.dt.strftime("%I:%M %p"))
        except:
            continue
        location = event.get('location')
        topic = event.get('summary')
        description = event.get('DESCRIPTION')
        #get rid of html tags
        p = re.compile(r'<.*?>')
        p.sub('', str(description))

        events_dict[i] = {
              'date': str(date.dt.strftime("%x")),
              'time': time,
              'topic': str(topic).strip(), 
              'location': str(location),
              'description': re.compile(r'<.*?>').sub('', str(description)).replace('&nbsp;','')
          }
        
    return events_dict

def ical2eventList(ical):
    context = ssl._create_unverified_context()
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    hdr={'User-Agent':user_agent,} 
    req=urllib.request.Request(ical,None,hdr)
    response = urllib.request.urlopen(req,context = context).read() 
    cal = Calendar.from_ical(response)
    events_dict = []
    #iterrate through events in cal with new events from each 'vevent' 
    #add time,date, title and details to events_dict    
    for i, event in enumerate(cal.walk('vevent')):
        date = event.get('dtstart')
        try:
            time = str(date.dt.strftime("%I:%M %p"))
        except:
            continue
        location = event.get('location')
        topic = event.get('summary')
        description = event.get('DESCRIPTION')
        #get rid of html tags
        p = re.compile(r'<.*?>')
        p.sub('', str(description))

        events_dict.append(
            {
              'date': str(date.dt.strftime("%x")),
              'time': time,
              'topic': str(topic).strip(), 
              'location': str(location),
              'description': re.compile(r'<.*?>').sub('', str(description)).replace('&nbsp;','')
            }
        )
        
    return events_dict


# %%




