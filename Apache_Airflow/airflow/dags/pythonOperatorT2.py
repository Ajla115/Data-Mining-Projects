from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    print(f"Weight: {weight} kg, Height: {height} m")
    print(f"Calculated BMI: {bmi:.2f}")

    if bmi < 18.5:
        print("BMI Category: Underweight")
    elif 18.5 <= bmi < 24.9:
        print("BMI Category: Normal weight")
    elif 25 <= bmi < 29.9:
        print("BMI Category: Overweight")
    else:
        print("BMI Category: Obesity")

with DAG(
    dag_id="bmi_calculation",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
) as dag:

    bmi_task = PythonOperator(
        task_id="calculate_bmi_task",
        python_callable=calculate_bmi,
        op_kwargs={"weight": 70, "height": 1.75}
    )

    bmi_task
