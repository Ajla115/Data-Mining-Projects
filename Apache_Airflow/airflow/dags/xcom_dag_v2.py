from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner" : "ajlakorman",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=2)

}
def greet(ti):
    first_name = ti.xcom_pull(task_ids = "get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids = "get_name", key="last_name")
    age = ti.xcom_pull(task_ids = "get_age", key="age")

    print("Hello, world. I am ", first_name, last_name, " and I am ", age, " years old.")

def get_name(ti):
    ti.xcom_push(key='first_name', value="Ajla")
    ti.xcom_push(key='last_name', value="Korman")
    
def get_age(ti):
        ti.xcom_push(key='age', value=22)


with DAG (

    dag_id = "xcom_dag_v2",
    default_args = default_args,
    description = "This is the first dag with python operator",
    start_date = datetime(2025, 2, 19, 12),
    schedule_interval = "@daily"

) as dag: 

    task1 = PythonOperator (
        task_id = "greet",
        python_callable = greet

    )

    task2 = PythonOperator (
        task_id = "get_name",
        python_callable = get_name

    )

    task3 = PythonOperator (
        task_id = "get_age",
        python_callable = get_age

    )

    [task2, task3] >> task1

