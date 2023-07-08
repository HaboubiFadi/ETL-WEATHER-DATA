
from sqlalchemy import String,Column,Date,Integer
from base import  Base 

from sqlalchemy.orm import relationship
class Location(Base):

    __tablename__ = 'locations'
    
    __table_args__ = {'extend_existing': True}




    id=Column(Integer,primary_key=True)
    name=Column(String)
    country=Column(String)
    lat=Column(Integer)
    lon=Column(Integer)
    last_update_day=Column(Date)


    hist_days=relationship('Hist_day',uselist=True,cascade='all, delete-orphan')
    forcast_days=relationship('Forcast_day',uselist=True,cascade='all, delete-orphan')
    currents=relationship('Current',uselist=True,cascade='all, delete-orphan')


    def __init__(self,serie):
        self.name=serie['name']
        self.country=serie['country']
        self.lat=serie['lat']
        self.lon=serie['lon']
        self.last_update_day=serie['last_update_day']


    def set_updated_time(self,datetime):
        self.last_update_day=datetime
    
    def get_name(self):
        return self.name    
    def get_last_time_updated(self):
        return self.last_update_day
