#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# In[8]:


class Database():
    engine = create_engine("sqlite:///events.db")
    Session = sessionmaker(bind = engine)
    session = Session()
    
    
    Base = declarative_base()

    class Event(Base):
        __tablename__ = 'event'
        id = Column('id',Integer, primary_key = True)
        district = Column(Integer)
        title = Column(String(100))
        date = Column(String(50))
        details = Column(String(1000))
        time = Column(String(50))

        def __init__(self, title, date, details,time,district):
            self.title = title
            self.date = date
            self.details = details
            self.time = time
            self.district = district

        #for print    
        def __repr__(self):
            return f'{self.title} - {self.date}: {self.time}\n {self.details} - {self.district}'
        
    Base.metadata.create_all(engine)
    distict = 100
    
    def __init__(self, district):
        self.district = district
        
    def addRow(self, title, date, details, time):
        """appends an event to the existing database 
        """
        row = self.Event(title = title, date = date, details = details, district = self.district, time = time)
        self.session.add(row)
        self.session.commit()
        
    def getAllRows(self):
        return list(self.session.query(self.Event))
    
    def getDistrictRows(self, district = None):
        if district is None:
            district = self.district
            
        return list(self.session.query(self.Event).filter(self.Event.district == district))


# In[9]:


if __name__ == '__main__':
    database = Database(101)
    database.addRow("title", "1/1/2022", 'details here', '12:00')
    database.getAllRows()


# In[ ]:




