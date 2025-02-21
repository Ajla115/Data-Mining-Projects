from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

@dag(
    dag_id="taskflow_student_grades",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
)
def student_grades_etl():

    @task(multiple_outputs=True)
    def get_scores():
        return {
            "Alice": 85,
            "Bob": 72,
            "Charlie": 90,
            "Diana": 65
        }

    @task()
    def calculate_grades(scores):
        grades = {}
        for student, score in scores.items():
            if score >= 90:
                grades[student] = "A"
            elif score >= 80:
                grades[student] = "B"
            elif score >= 70:
                grades[student] = "C"
            elif score >= 60:
                grades[student] = "D"
            else:
                grades[student] = "F"
        return grades

    @task()
    def display_results(grades):
        for student, grade in grades.items():
            print(f"{student} received a grade of {grade}.")

    scores = get_scores()
    grades = calculate_grades(scores)
    display_results(grades)

grades_dag = student_grades_etl()
