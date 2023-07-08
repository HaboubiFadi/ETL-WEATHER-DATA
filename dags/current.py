from sqlalchemy import String,Column,DateTime,Integer,ForeignKey
from base import  Base 
from sqlalchemy.orm import relationship

class Current(Base):
    __tablename__='current'
    __table_args__ = {'extend_existing': True}




    id= Column(Integer,primary_key=True)
    temp_c=Column(Integer)
    
    

    
    humidity=Column(Integer)
    condition=Column(String)
    date=Column(String)
    location_id=Column(Integer,ForeignKey('locations.id'))


    def __init__(self,serie):

        self.temp_c=float(serie['temp_c'])
   
        self.humidity=float(serie['humidity'])
        self.condition=str(serie['condition'])
        self.date=str(serie['last_updated'])
