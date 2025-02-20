
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

default_args = {
    'owner': 'ajlakorman',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'etl_example',
    default_args=default_args,
    description='A simple ETL example',
    schedule_interval='@daily',
)


def extract_data():
    df = pd.read_csv("/Users/ajlakorman/Desktop/Data-Mining-Projects/Billionaire Statistics Dataset Project/BillionairesStatisticsDataset.csv")
    return df

def transform_data(df):
    df['personName'] = df['personName'].str.upper()
    return df

def load_data(df):
    engine = create_engine('mysql://username:password@localhost/mydatabase')
    df.to_sql('mytable', con=engine, if_exists='replace', index=False)



extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_task
