from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    "owner": "ajlakorman",
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

@dag(
    dag_id="taskflow_movie_ratings",
    default_args=default_args,
    start_date=datetime(2024, 2, 20),
    schedule_interval="@daily",
    catchup=False
)
def movie_rating_etl():

    @task(multiple_outputs=True)
    def get_movie_ratings():
        return {
            "Inception": 9,
            "Titanic": 8,
            "Avatar": 7,
            "The Room": 3,
            "Interstellar": 10
        }

    @task()
    def categorize_movies(ratings):
        categories = {}
        for movie, rating in ratings.items():
            if rating >= 9:
                categories[movie] = "Excellent"
            elif rating >= 7:
                categories[movie] = "Good"
            elif rating >= 5:
                categories[movie] = "Average"
            else:
                categories[movie] = "Poor"
        return categories

    @task()
    def display_movie_categories(categories):
        for movie, category in categories.items():
            print(f"{movie} is rated as {category}.")

    ratings = get_movie_ratings()
    categories = categorize_movies(ratings)
    display_movie_categories(categories)

movie_ratings_dag = movie_rating_etl()
