import random
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

def generate_and_analyze_numbers():
    numbers = [random.randint(1, 100) for _ in range(10)]
    even_count = sum(1 for n in numbers if n % 2 == 0)
    odd_count = 10 - even_count
    total_sum = sum(numbers)

    print(f"Generated Numbers: {numbers}")
    print(f"Even Numbers: {even_count}")
    print(f"Odd Numbers: {odd_count}")
    print(f"Total Sum: {total_sum}")


with DAG(
    dag_id="random_numbers_analysis",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
) as dag:

    analyze_task = PythonOperator(
        task_id="analyze_random_numbers",
        python_callable=generate_and_analyze_numbers
    )

    analyze_task
