import pandas as pd
from bs4 import BeautifulSoup
import unicodedata
import requests
import re
import lib.database as db
from lib.reconst import MONTH_REGEX
import datetime
from datetime import date
import lib.ical_scraper as ical_s
import lib.js_scraper as js_s
import lib.airtable_scraper as air_s
import subprocess
import sys
import glob

# Set the directory and the pattern for the .py files
directory = "CB_scrapers"
pattern = "1*.py"

# Use glob.glob() to get a list of .py files that match the pattern
file_list = glob.glob(f"{directory}/{pattern}")

for file in file_list:
    print(f"Running: {file}")
    
    # Use subprocess.run() to execute the Python file
    result = subprocess.run(["python", file], capture_output=True, text=True)

    # Print the output of the executed script
    print("Output:", result.stdout)
    print("Errors:", result.stderr)


