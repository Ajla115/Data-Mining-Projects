from airflow import DAG
from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

@dag(
    dag_id="dag_with_taskflow_api",
    default_args=default_args,
    start_date=datetime(2021, 10, 26),
    schedule_interval="@daily",
    catchup=False
)
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_user_details():
        return {
            "first_name": "Ajla",
            "last_name": "Korman",
            "age": 22
        }

    @task()
    def greet(first_name, last_name, age):
        print(f"Hello, my name is {first_name} {last_name} and I am {age} years old.")

    user_details = get_user_details()
    greet(
        first_name=user_details['first_name'],
        last_name=user_details['last_name'],
        age=user_details['age']
    )

greet_dag = hello_world_etl()
