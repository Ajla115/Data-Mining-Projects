from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    dag_id="bash_operator_disk_usage",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
) as dag:

    check_disk_usage = BashOperator(
        task_id="check_disk_usage",
        bash_command="df -h",
    )

    current_time = BashOperator(
        task_id="display_current_time",
        bash_command="date"
    )

    check_network = BashOperator(
        task_id="check_network_connections",
        bash_command="netstat -an | head -10"
    )

    check_disk_usage >> current_time >> check_network
