from base import Base
from sqlalchemy import Column,Integer,ForeignKey,Date,String

class Forcast_day(Base):
    __tablename__='forcast_days'
    __table_args__ = {'extend_existing': True}




    id= Column(Integer,primary_key=True)
    max_temp=Column(Integer)
    

    min_temp=Column(Integer)
    avg_temp=Column(Integer)
    humidity=Column(Integer)
    condition=Column(String)
    date=Column(Date)
    location_id=Column(Integer,ForeignKey('locations.id'))


    def __init__(self,serie):

        self.max_temp=serie['maxtemp_c']
        self.min_temp=serie['mintemp_c']
        self.avg_temp=serie['avgtemp_c']
        self.humidity=serie['avghumidity']
        self.condition=serie['condition']
        self.date=serie['date']
