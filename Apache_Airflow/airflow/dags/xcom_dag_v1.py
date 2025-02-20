from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner" : "ajlakorman",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=2)

}
def greet(age, ti):
    name = ti.xcom_pull(task_ids = "get_name")
    print("Hello, world. I am ", name, " and I am ", age, " years old.")

def get_name():
    return "Ajla"

with DAG (

    dag_id = "xcom_dag_v1",
    default_args = default_args,
    description = "This is the first dag with python operator",
    start_date = datetime(2025, 2, 19, 12),
    schedule_interval = "@daily"

) as dag: 

    task1 = PythonOperator (
        task_id = "greet",
        python_callable = greet,
        op_kwargs = {"age" : 22}

    )

    task2 = PythonOperator (
        task_id = "get_name",
        python_callable = get_name

    )

    task2 >> task1

