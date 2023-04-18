import sys
import os


# +
def import_airtable_scraper():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    import airtable_scraper
    
    return airtable_scraper

def import_database():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    import database
    
    return database

def import_ical_scraper():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    import ical_scraper
    
    return ical_scraper

def import_js_scraper():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    import js_scraper
    
    return js_scraper

def import_pdf_scraper():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    import pdf_scraper
    
    return pdf_scraper

def import_month_regex_var():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    from reconst import MONTH_REGEX
    
    return MONTH_REGEX

def import_date_regex_var():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    from reconst import date_regex
    
    return date_regex

def import_time_regex_var():
    # Get the grandparent directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add parent_directory_B to sys.path
    parent_directory_B = os.path.join(grandparent_directory, 'lib')
    sys.path.append(parent_directory_B)

    # Import script_B.py as a module
    from reconst import time_regex
    
    return time_regex
