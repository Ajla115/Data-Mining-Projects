from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random
import math

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

def generate_random_number(ti):
    number = random.randint(1, 20)
    print(f"Generated Random Number: {number}")
    ti.xcom_push(key="random_number", value=number)

def calculate_factorial(ti):
    number = ti.xcom_pull(task_ids="generate_random_number", key="random_number")
    if number:
        factorial = math.factorial(number)
        print(f"The factorial of {number} is {factorial}")
    else:
        print("No number found in XCom!")

with DAG(
    dag_id="xcom_random_number_factorial",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
) as dag:

    generate_task = PythonOperator(
        task_id="generate_random_number",
        python_callable=generate_random_number
    )

    factorial_task = PythonOperator(
        task_id="calculate_factorial",
        python_callable=calculate_factorial
    )

    generate_task >> factorial_task
