from airflow import  DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from base import Session
import pandas as pd
from location import Location
from hist_day import Hist_day
from current import Current

from forcast_day import Forcast_day

from tools import trigger_database ,extract_updated_data ,clear_memory


from airflow.decorators import dag,task
from datetime import datetime,timedelta
from forcast_data_fetch import save_forcastas_pd_csv



defaults_arg={'owner':'haboubi','retries':2,'retry_delay':timedelta(minutes=1)}

def trigger_database_dag(ti):
    session =Session()
    locations=session.query(Location).all()
    info=trigger_database(locations)
    ti.xcom_push(key='info',value=info)

     
def extract_data(ti):
    info=ti.xcom_pull(key='info')
    extract_updated_data(info)
    save_forcastas_pd_csv()


def update_location_entite(loc):
    directory_hist='city_hist_updated/'+loc.get_name()+'.csv'
    directory_forc='forcast/'+loc.get_name()+'.csv'
    forc_data=[]
    hist_days_csv=pd.read_csv(directory_hist,sep='\t')
    forcast_days_csv=pd.read_csv(directory_forc,sep='\t')
   
    for i in range(len(hist_days_csv)):
        loc.hist_days.append(Hist_day(hist_days_csv.iloc[i]))
    for i in range(len(forcast_days_csv)):
        forc_data.append(Forcast_day(forcast_days_csv.iloc[i]))  
    
    loc.forcast_days=forc_data   

    return loc



def load_updated_data_db():
    directory='updated_locations.csv'
    session=Session()
    locations_csv=pd.read_csv(directory,sep='\t')
    for i in range(len(locations_csv)):
        print('debug prb:',locations_csv.iloc[i]['name'])
        loc=session.query(Location).filter(Location.name == locations_csv.iloc[i]['name']).first()
        loc=update_location_entite(loc)
        loc.set_updated_time(locations_csv.iloc[i]['last_update_day'])
        print('last_time_updated:',loc.get_last_time_updated())
        session.add(loc)
    session.commit()
    session.close()
    return 0    


        
    











with DAG (
    dag_id='updated_day_hist_forcast_data',
    default_args=defaults_arg,
    schedule='@daily',
    start_date=datetime(2023,7,1),
    catchup=True





) as dag:
    # task_name=trigger_db_dag:
    # this trigger is used for fetch all locations , and only keep 2 features(name,last_updated_day)
    # pushing the result(a dictionary into a XCOM to move the variable between tasks)
    # "python_callable=trigger_database_dag" used the trigger_database_dag as a function
    trigger_db_dag =PythonOperator(
        python_callable=trigger_database_dag,
        task_id='trigger_db'

        )
    # task=extract_updated_data_dag
    # save current data into csv files to be used in the next task='load_updated_data_db'  
    extract_updated_data_dag=PythonOperator(
          python_callable=extract_data,
          task_id='extract_updated_data'



    )
     # task='load_updated_data_dag'
    # detail:loading updated data from the csv files in the 'current' directory into database
    load_updated_data_dag =PythonOperator(
        python_callable=load_updated_data_db,
        task_id='load_updated_data_hist_forcast'

    )
     # task='clear_memory_hist_csv_dag'
    # detail:clear the './city_hist_updated' directory 
    clear_memory_hist_csv_dag =PythonOperator(
        python_callable=clear_memory,
        task_id='clear_memory_hist_csv_dag',
        op_kwargs={'dir':'./city_hist_updated'}

    # task='clear_memory_forca_csv_dag'
    # detail:clear the './forcast' directory   
    )
    clear_memory_forca_csv_dag =PythonOperator(
        python_callable=clear_memory,
        task_id='clear_memory_updated_forc',
        op_kwargs={'dir':'./forcast'}

    )
    
    trigger_db_dag >> extract_updated_data_dag >> load_updated_data_dag >> [clear_memory_hist_csv_dag,clear_memory_forca_csv_dag]