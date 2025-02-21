from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'ajlakorman',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'simple_etl_billionaires',
    default_args=default_args,
    description='Simple ETL example to filter billionaires by country',
    schedule_interval='@daily',
    catchup=False
)

def extract_data():
    df = pd.read_csv("/Users/ajlakorman/Desktop/Data-Mining-Projects/Billionaire Statistics Dataset Project/BillionairesStatisticsDataset.csv")
    print(f"Extracted {len(df)} records.")
    return df.to_dict()

def filter_us_billionaires(ti):
    data = ti.xcom_pull(task_ids='extract_data')
    df = pd.DataFrame.from_dict(data)
    
    us_billionaires = df[df['country'] == 'United States']
    print(f"Found {len(us_billionaires)} billionaires from the United States.")
    print(us_billionaires[['personName', 'finalWorth']])
    return us_billionaires.to_dict()

def load_data(ti):
    data = ti.xcom_pull(task_ids='filter_us_billionaires')
    df = pd.DataFrame.from_dict(data)
    print(f"Loading {len(df)} U.S. billionaires into output.")
    print(df[['personName', 'finalWorth']])

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

filter_task = PythonOperator(
    task_id='filter_us_billionaires',
    python_callable=filter_us_billionaires,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

extract_task >> filter_task >> load_task
