#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pdf2image import convert_from_path
import cv2
import pytesseract
import matplotlib.pyplot as plt
import tabula 
import re
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import glob
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import time as time_lib


# In[2]:


def mark_region(image_path):
    
    im = cv2.imread(image_path)
    img = Image.open(image_path)
    width, height = img.size
    max_w = width-100

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(im, (x,y), (max_w, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (max_w, y+h)])

        if y >= 2400 and x<= 2000:
            image = cv2.rectangle(im, (x,y), (max_w, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (max_w, y+h)]) #Why Doesnt it just use w????


    return image, line_items_coordinates


# In[3]:


#url = 'https://www.cb14brooklyn.com/category/meetings/'
def pdf_scraper(url):
    link_scores = []
    currentMonth = datetime.now().strftime('%B').lower()
    currentMonth1 = datetime.now().strftime('%h').lower()
    currentYear = datetime.today().year
    #convert the webpage to soup
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = []
    #find the webpage body with event details
    for link in soup.find_all('a'):
        if re.search('\.pdf$', link.get('href')):
            links.append(link.get('href'))
    for i,link in enumerate(links):
        score = 0
        link = link.lower()
        if re.search(currentMonth, link):
            score += 1
        elif re.search(currentMonth1, link):
            score += 1
        if re.search(str(currentYear), link):
            score += 1
        if re.search('calendar', link):
            score += 1
        if re.search('update', link):
            score += 1
        link_scores.append(score)
    index_max = max(range(len(link_scores)), key=link_scores.__getitem__)
    pdf_url = links[index_max]
    if pdf_url.startswith('/'):
        pdf_url = 'https://www.nyc.gov' + pdf_url 
    pdf_url


    # In[4]:


    driver = webdriver.Chrome(ChromeDriverManager().install())
    service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"download.default_directory" : os.getcwd()}
    chrome_options.add_experimental_option('prefs', {"download.default_directory" : os.getcwd(),
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
    driver = webdriver.Chrome(service=service, options=chrome_options, executable_path=(str(os.getcwd()) + 'chromedriver.exe'))
    driver.get(pdf_url)
    time_lib.sleep(5)
    list_of_files = glob.glob(str(os.getcwd()) + '\\*.pdf') # * means all if need specific format then *.csv
    pdf_cal = max(list_of_files, key=os.path.getctime)
    driver.quit()

    pdfs = pdf_cal
    pages = convert_from_path(pdfs, 300)
    jpg_pages = []

    for i, page in enumerate(pages):
        image_name = "Page_" + str(i) + ".jpg"  
        page.save(image_name, "JPEG")
        jpg_pages.append(image_name)


    # In[8]:


    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    max_score = 0
    max_index = 0
    max_page = 0
    for page_index, page in enumerate(jpg_pages): 
        pic,coordinates = mark_region(str(os.getcwd()) + '\\' + page)
        texts = []
        for c in coordinates:
        # load the original image
            image = cv2.imread(str(os.getcwd()) + '\\' + page)

            # cropping image img = image[y0:y1, x0:x1]
            img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

            # convert the image to black and white for better OCR
            ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

            # pytesseract image to string to get results
            text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
            texts.append(text.lower())
        area_scores = []
        for text in texts:
            score = 0

            #contains a number 1-30
            nums = []
            for i in range(1,32):
                nums.append(str(i)+'\s')
            for i in nums:
                if re.search(i, text):
                    score += 1

            #contains a time
            for time in re.findall(r'(1[0-2]|0?[1-9]):([0-5]?[0-9])(●?[ap]m)?',text):
                score += 1

            for dayOfWeek in re.findall(r'\b((mon|tues|wed(nes)?|thur(s)?|fri|sat(ur)?|sun)(day)?)\b',text):
                score += 1

            area_scores.append(score)

        index_max = max(range(len(area_scores)), key=area_scores.__getitem__)
        if area_scores[index_max] > max_score:
            max_score = area_scores[index_max]
            max_index = index_max
            max_page = page_index


    pic,coordinates = mark_region(str(os.getcwd()) + '\\' + jpg_pages[max_page])
    c = coordinates[max_index]
    

    dfs = tabula.read_pdf(pdf_cal, pandas_options = {'header': None},  pages = max_page+1, area = [c[0][1]*72/300, c[0][0]*72/300, c[1][1]*72/300, c[1][0]*72/300], lattice = True)
    os.remove(pdf_cal)
    for page in jpg_pages:
        os.remove(str(os.getcwd()) + '\\' + page)
    return dfs






