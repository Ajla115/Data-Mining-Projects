from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

def generate_two_strings(ti):
    string1 = "Airflow"
    string2 = "Python"
    print(f"Generated Strings: {string1}, {string2}")
    ti.xcom_push(key="string1", value=string1)
    ti.xcom_push(key="string2", value=string2)

def reverse_strings(ti):
    string1 = ti.xcom_pull(task_ids="generate_two_strings", key="string1")
    string2 = ti.xcom_pull(task_ids="generate_two_strings", key="string2")

    if string1 and string2:
        reversed1 = string1[::-1]
        reversed2 = string2[::-1]

        print(f"Original String 1: {string1}, Reversed: {reversed1}")
        print(f"Original String 2: {string2}, Reversed: {reversed2}")
    else:
        print("Strings not found in XCom!")

with DAG(
    dag_id="xcom_reverse_strings",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
) as dag:

    generate_strings_task = PythonOperator(
        task_id="generate_two_strings",
        python_callable=generate_two_strings
    )

    reverse_strings_task = PythonOperator(
        task_id="reverse_strings",
        python_callable=reverse_strings
    )

    generate_strings_task >> reverse_strings_task
