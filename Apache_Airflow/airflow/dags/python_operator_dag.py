from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner" : "ajlakorman",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=2)

}
def greet():
    print("Hello, world!")

with DAG (

    dag_id = "python_operator_dag_v01",
    default_args = default_args,
    description = "This is the first dag with python operator",
    start_date = datetime(2025, 2, 19, 12),
    schedule_interval = "@daily"


) as dag: 

    task1 = PythonOperator (
        task_id = "greet",
        python_callable = greet

    )

    task1

