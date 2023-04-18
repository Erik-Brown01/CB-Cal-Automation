#!/usr/bin/env python
# coding: utf-8
# %%
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
import numpy as np


# %%


def airtable_scraper(url):
    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"download.default_directory" : os.getcwd()}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options, executable_path=(str(os.getcwd()) + 'chromedriver.exe'))
    
    driver.get(url)

    driver.implicitly_wait(100)

#     elements = driver.find_elements(by=By.CSS_SELECTOR, value=".ml-half")

#     for element in elements:
#         text = element.text
#         if text == 'Download CSV':
#             element.click()

    driver.find_element(By.XPATH, '//*[@id="embedBottomBarContainer"]/div/div/a[2]').click()

    #time.sleep(5)
    #driver.implicitly_wait(5000)
    
    max_retries = 10
    attempts = 0
    success = False

    while not success and attempts < max_retries:
        try:
            list_of_files = glob.glob(str(os.getcwd()) + '\\*.csv') # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            df = pd.read_csv(latest_file)
            os.remove(latest_file)
            #print(str(os.getcwd()) + '\\*.csv')
            driver.quit()
            success = True  # If the code block executes without errors, set success to True
        except Exception as e:
            time.sleep(5)
            attempts += 1
            #print(f"Attempt {attempts} failed with error: {e}")
            if attempts >= max_retries:
                 return e
                
    return df
               


    
    df[['date', 'time']] = df['Date & Time'].str.split(' ', expand=True)
    df['description'] = df.apply(lambda row: " \n ".join(["{}: {}".format(col, row[col]) for col in ['Register to Attend', 'Agenda', 'Minutes', 'Recording', 'Presentations'] if not pd.isna(row[col]) and row[col] != '']), axis=1)
    df = df.drop(columns=['Date & Time', 'Register to Attend', 'Minutes', 'Recording', 'Presentations', 'Agenda'])
    #df = df[~(df['date'] < datetime.date.today().replace(day=1, month=(datetime.date.today().month-3)))].reset_index()
    events_dict = {}
    #iterrate through events in cal with new events from each 'vevent' 
    #add time,date, title and details to events_dict    
    
#     for index, row in df.iterrows():
#         events_dict[index] = {
#                   'date': str(row['date']),
#                   'time': str(row['time']),
#                   'topic': str(row['Name']), 
#                   'location': str(row['Location']),
#                   'description': str(row['Agenda'])
#               }

    df.columns = [col.lower() for col in df.columns]
    df = df.rename(columns = {"name": "topic"})
    #df = df.drop(columns = ['index'])
    df['date'] = datetime.strptime(date_str, "%m/%d/%Y").strftime("%m/%d/%y")
    
    events_dict = df.to_dict('records')
    
    
    return events_dict


# %%
