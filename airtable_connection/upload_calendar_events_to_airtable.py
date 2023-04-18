from airtable import Airtable
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Load environment variables from the .env file
load_dotenv(r'C:\Users\ebroh\BetaNYC\CB-Cal-Automation\airtable_connection\.env.txt')

# SQLAlchemy database model
Base = declarative_base()

class CalendarEvent(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    district = Column(Integer)
    date = Column(String)      # Store date as a string
    time = Column(String)      # Store time as a string
    title = Column(String)
    details = Column(String)

# Retrieve the DATABASE_URL from the .env file
DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Airtable API configuration
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
AIRTABLE_TABLE_NAME = 'CalendarEvents'

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)

# Upload calendar events to Airtable
def upload_events_to_airtable():
    events = session.query(CalendarEvent).all()

    for event in events:

        airtable_record = {
            'ID': event.id,
            'District': event.district,
            'Date': event.date,
            'Time': event.time,
            'Title': event.title,
            'Details': event.details,
        }

        airtable.insert(airtable_record)

if __name__ == "__main__":
    upload_events_to_airtable()


