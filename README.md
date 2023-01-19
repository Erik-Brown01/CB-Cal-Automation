# CB Cal Automation

A project to automate the pulling of all community board calendars for upcoming meetings. This project stemmed from previous work done by [Eric Butler](https://github.com/codebutler/59boards). 

Please explore [Block Party](https://blockparty.studio/) for a search through community board recording transcripts!

---

The repo contains various scripts that scrape, parses, and standardize calendar formats for:

- html
- ical
- gcal
- custom json
- airtable
- pdf (text and image-based)

For boards that don't have parsable formats dates for meetings are hardcoded.

### Install 

`conda create --name <env_name> --file requirements.txt`

or

`conda create --name <env_name>` then

`conda install -c conda-forge notebook sqlalchemy selenium pandas matplotlib pillow tabula-py pytesseract opencv beautifulsoup4 pdf2image webdrivermanager`

`pip3 install webdriver-manager`