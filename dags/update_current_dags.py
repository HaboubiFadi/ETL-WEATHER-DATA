from airflow import  DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from base import Session
import pandas as pd
from location import Location
from current import Current
from datetime import datetime
from tools import trigger_database ,extract_updated_data ,clear_memory
from current_data_fetch import save_current_pd_csv


from airflow.decorators import dag,task
from datetime import datetime,timedelta
from forcast_data_fetch import save_forcastas_pd_csv



defaults_arg={'owner':'haboubi','retries':2,'retry_delay':timedelta(minutes=1)}



def trigger_database_dag(ti): 
    session =Session()
    locations=session.query(Location).all()
    info=trigger_database(locations)
    ti.xcom_push(key='info',value=info)

# task=extract_data
# save current data into csv files to be used in the next task='update_location_entite'     
def extract_data(ti):
    save_current_pd_csv()

#task='update_location_entite'
# using the XCOM 
def update_location_entite(loc):
    directory_hist='current/'+loc.get_name()+'.csv'
    forc_data=[]
    current=pd.read_csv(directory_hist,sep='\t')
   
    for i in range(len(current)):
        cur=Current(current.iloc[i])
        loc.currents.append(cur)
   
    

    return loc



def load_updated_data_db(ti):
    info=ti.xcom_pull(key='info')
    session= Session()
    for i in info:
        print(i)
        loc=session.query(Location).filter(Location.name == i[0]).first()
        loc=update_location_entite(loc)
        session.add(loc)
        session.commit()
        session.close()

    
    return 0    


        
    











# DAG_description:'update the current entite into the data base'
# scheduled every 20 minutes 

with DAG (
    dag_id='update_current_data_10',
    default_args=defaults_arg,
    schedule='*/20 * * * *',
    start_date=datetime(2023,7,6),
    catchup=False





) as dag:
    # task_name=trigger_db_dag:
    # this trigger is used for fetch all locations , and only keep 2 features(name,last_updated_day)
    # pushing the result(a dictionary into a XCOM to move the variable between tasks)
    # "python_callable=trigger_database_dag" used the trigger_database_dag as a function
    trigger_db_dag =PythonOperator(
        python_callable=trigger_database_dag,
        task_id='trigger_location_db'

        )
    # task=extract_updated_data_dag
    # save current data into csv files to be used in the next task='load_updated_data_db'   
    extract_updated_data_dag=PythonOperator(
          python_callable=extract_data,
          task_id='extract_current_data'



    )
    # task='load_updated_data_dag'
    # detail:loading updated data from the csv files in the 'current' directory into database
    load_updated_data_dag =PythonOperator(
        python_callable=load_updated_data_db,
        task_id='load_current_data'

    )
    # task='clear_memory_current_dag'
    # detail:clear the './current' directory 
    clear_memory_current_dag =PythonOperator(
        python_callable=clear_memory,
        task_id='clear_memory_current_dag',
        op_kwargs={'dir':'./current'}

    )
    
    
    trigger_db_dag >> extract_updated_data_dag >> load_updated_data_dag >> clear_memory_current_dag