# import PyPDF2
# from pdf2image import convert_from_path
# import cv2
# import pytesseract
# import matplotlib.pyplot as plt
# import tabula 
# import re
# from PIL import Image, ImageFilter, ImageDraw
# import numpy as np
# import glob
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from datetime import datetime, date
# from selenium.webdriver.chrome.options import Options
# import requests
# from bs4 import BeautifulSoup, NavigableString, Tag
# import time as time_lib
# import sys

import sys
import PyPDF2
import pdf2image
import pytesseract
from PIL import Image
import tabula
import os
import sys
import requests
from datetime import datetime, date
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import cv2
import numpy as np


def findCalendarPDFLink(url, month = None, year = None):
    link_scores = []
    
    if year == None:   
        currentYear = datetime.today().year

    else:
        currentYear = int(year)
        
    if month == None:
        currentMonth = datetime.now().strftime('%B').lower()
        currentMonth1 = datetime.now().strftime('%b').lower()
        currentMonth2 = datetime.now().strftime('%m').lower()
    else:
        month_year_str = f"{month} {currentYear}"
        month_dt = datetime.strptime(month_year_str, '%B %Y')
        currentMonth = month_dt.strftime('%B').lower()
        currentMonth1 = month_dt.strftime('%b').lower()
        currentMonth2 = month_dt.strftime('%m').lower()
        
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
            score += 5
        elif re.search(currentMonth1, link):
            score += 5
        elif re.search(currentMonth2, link):
            score += 2
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

    return pdf_url


def download_pdf(url, filename=None):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to download the PDF. Status code: {response.status_code}")
        return None

    if filename is None:
        filename = os.path.basename(url)
        
    pdf_path = os.path.join(os.getcwd(), filename)
    with open(pdf_path, 'wb') as file:
        file.write(response.content)
        
    print(f"PDF downloaded successfully as {filename}")
    return pdf_path

# Ensure the path to the tesseract executable is in your system's PATH variable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def is_calendar_section(text):
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    days_found = [day for day in days_of_week if day in text.lower()]

    digit_count = len(re.findall(r'\d', text))

    return (len(days_found) >= 5) or (digit_count >= 20)



def is_calendar_contour(contour, img_width, img_height, img):
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h

    # if not (0.5 < aspect_ratio < 2 and img_width * 0.5 < w < img_width * 0.95 and img_height * 0.5 < h < img_height * 0.95):
    #     return False

    cropped_image = img[y:y + h, x:x + w]
    text = pytesseract.image_to_string(cropped_image)
    print(text)

    return is_calendar_section(text)

def get_calendar_coordinates(image):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    calendar_contour = None
    #print(contours)

    for contour in contours:
        if is_calendar_contour(contour, gray.shape[1], gray.shape[0], gray):
            calendar_contour = contour
            break

    if calendar_contour is None:
        return None

    x, y, w, h = cv2.boundingRect(calendar_contour)

    return {
        'top': y,
        'left': x,
        'width': w,
        'height': h,
        'bottom': y + h,
        'right': x + w
    }


def extract_calendar_from_pdf(pdf_path):
    calendar_data = None

    try:
        pdf = PyPDF2.PdfFileReader(pdf_path)
        num_pages = pdf.getNumPages()

        for page in range(num_pages):
            images = pdf2image.convert_from_path(pdf_path, first_page=page + 1, last_page=page + 1, dpi = 300)

            for img in images:
                coords = get_calendar_coordinates(img)
                if coords:
                    df = tabula.read_pdf(
                        pdf_path,
                         pandas_options = {'header': None},
                        area=[
                            coords['top']*72/300,
                            coords['left']*72/300,
                            coords['bottom']*72/300,
                            coords['right']*72/300
                        ],
                        pages=page + 1,
                        multiple_tables=False,
                        lattice = True
                    )[0]

                    calendar_data = df
                    break  # Stop looking for the calendar section after finding one

            if calendar_data is not None:
                break

    except Exception as e:
        print(f"Error: {e}")

    return calendar_data

def pdf_scraper(url, month = None, year = None):
    pdf_url = findCalendarPDFLink(url, month, year)
    pdf_path = download_pdf(pdf_url)
    calendar_data = extract_calendar_from_pdf(pdf_path)
    if month == None:
        month = datetime.now().strftime('%B').lower()
    if year == None:
        year = datetime.today().year
    if calendar_data is not None:
        return calendar_data, month, year
    else:
        print("Calendar not found.")

