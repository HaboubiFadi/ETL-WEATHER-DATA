from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow import DAG
from datetime import datetime,timedelta
default_args={
    'owner':'haboubi',
    'retires':5,
    'retry_delay':timedelta(minutes=2)
}
with DAG(
    dag_id='cnt_to_db',
    default_args=default_args,
    start_date=datetime(2023,6,30),
    schedule_interval='0 0 * * *'

    )as dag:
        task1 = PostgresOperator(
                task_id='create_postgres_table',
                postgres_conn_id='postgres_localhost',
                sql="""
                create table if not exists dag_runs_1 (
                id SERIAL,
                dt date,
                dag_id character varying,
                primary key (id)

                )
                
                
                """
        )
        task2= PostgresOperator(
                task_id='insert_into_table',
                postgres_conn_id='postgres_localhost',
                sql="""
                insert into dag_runs_1 (dt, dag_id) values ('{{ ds }}','{{ dag.dag_id }}')
                
                """
                )
        task1 >> task2
    