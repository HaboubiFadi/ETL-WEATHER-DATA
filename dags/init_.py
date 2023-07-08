from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
import sys
from hist_day import Hist_day
from location import Location
from current import Current

from hist_day_data_fetch import save_pd_csv
from forcast_data_fetch import save_forcastas_pd_csv

from tools import location_fill_liste , clear_memory
from base import Session, engine, Base
 
# adding Folder_2 to the system path

default_arg={'owner':'haboubi','retries':5,'retry_delay':timedelta(minutes=1)}
# initiate the database variables 
# drop all existing tables 
# initiate the entites mapping with tables   
# initiate database with all th historical and forecasting data from that moment
def load_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    locs=location_fill_liste()
    session.add_all(locs)
    session.commit()
    session.close()






with DAG(
    dag_id='init_db',
    description='Create tables and fill it with historical data',
    schedule='@once',
    start_date=datetime(2023,7,1)


) as dag :
    # Extract Historical_data from API weather and tranforme it and save it into .csv files 
    Extract_hist_data_from_api = PythonOperator(
        task_id='extract_hist_data_id',
        python_callable=save_pd_csv,
        
    )
    # Extract forcasting_data from API weather and tranforme it and save it into .csv files 

    Extract_forcast_data_from_api = PythonOperator(
        task_id='extract_forc_data_id',
        python_callable=save_forcastas_pd_csv,
        
    )
    # load the data into the database
    Load_data_into_db =PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )
    # clear existing directory (Hist_data) 
    flush_hist=PythonOperator(
        task_id='clear_memory_hist',
        python_callable=clear_memory
    )
    # clear existing directory (Forcast) 

    flush_forcast=PythonOperator(
        task_id='clear_memory_forecst',
        python_callable=clear_memory,
        op_kwargs={'dir':'./forcast'}
    )
    
    
    [Extract_hist_data_from_api,Extract_forcast_data_from_api] >> Load_data_into_db >>[flush_hist,flush_forcast]

    