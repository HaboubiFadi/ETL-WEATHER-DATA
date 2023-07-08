# This is where we declare our database 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('postgresql://airflow_user:airflow_pass@localhost/airflow_db') # engine for database information

Session = sessionmaker(bind=engine) # Session for database manipulation

Base = declarative_base() # this variable is for mapping entites into database