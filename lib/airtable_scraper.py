#!/usr/bin/env python
# coding: utf-8

# In[75]:


from selenium.webdriver.common.by import By
import glob
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from datetime import date
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# In[76]:


def airtable_scraper(url):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"download.default_directory" : os.getcwd()}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options, executable_path=(str(os.getcwd()) + 'chromedriver.exe'))
    
    driver.get(url)

    driver.implicitly_wait(100)

    elements = driver.find_elements(by=By.CSS_SELECTOR, value=".ml-half")

    for element in elements:
        text = element.text
        if text == 'Download CSV':
            element.click()

    time.sleep(5)
    #driver.implicitly_wait(5000)

    list_of_files = glob.glob(str(os.getcwd()) + '\\*.csv') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    df = pd.read_csv(latest_file)
    os.remove(latest_file)
    #print(str(os.getcwd()) + '\\*.csv')
    driver.quit()
    
    df['date'] = pd.to_datetime(df['Date & Time']).dt.date
    df['time'] = pd.to_datetime(df['Date & Time']).dt.time
    df = df.drop(columns=['Date & Time', 'Register to Attend', 'Minutes', 'Recording', 'Presentations'])
    df = df[~(df['date'] < datetime.date.today().replace(day=1, month=(datetime.date.today().month-3)))].reset_index()
    events_dict = {}
    #iterrate through events in cal with new events from each 'vevent' 
    #add time,date, title and details to events_dict    
    
    for index, row in df.iterrows():
        events_dict[index] = {
                  'date': str(row['date']),
                  'time': str(row['time']),
                  'topic': str(row['Name']), 
                  'location': str(row['Location']),
                  'description': str(row['Agenda'])
              }
    
    return events_dict


# In[ ]:




