from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner" : "ajlakorman",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=2)


}
with DAG (

    dag_id = "our_first_dag_v3",
    default_args = default_args,
    description = "This is our first dag that we write",
    start_date = datetime(2025, 2, 19, 12),
    schedule_interval = "@daily"

) as dag: 
    task1 = BashOperator (
        task_id = "first_task",
        bash_command="echo 'Hello World, this is the first task'"

    )

    task2 = BashOperator (
        task_id = "second_task",
        bash_command="echo 'This is the second task that will run after the first one'"

    )

    task3 = BashOperator (
        task_id = "third_task",
        bash_command="echo 'This is the third task that will run at the same time as the second one'"
    )

    task1.set_downstream(task2)
    task1.set_downstream(task3)



