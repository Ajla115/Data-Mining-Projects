from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

def generate_string(ti):
    string = "HelloAirflow"
    print(f"Generated String: {string}")
    ti.xcom_push(key="input_string", value=string)

def analyze_string(ti):
    string = ti.xcom_pull(task_ids="generate_string", key="input_string")
    if string:
        length = len(string)
        vowels = sum(1 for char in string.lower() if char in "aeiou")
        consonants = length - vowels

        print(f"String: {string}")
        print(f"Length: {length}")
        print(f"Vowels: {vowels}")
        print(f"Consonants: {consonants}")
    else:
        print("No string found in XCom!")

with DAG(
    dag_id="xcom_string_analysis",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
) as dag:

    generate_string_task = PythonOperator(
        task_id="generate_string",
        python_callable=generate_string
    )

    analyze_string_task = PythonOperator(
        task_id="analyze_string",
        python_callable=analyze_string
    )

    generate_string_task >> analyze_string_task
