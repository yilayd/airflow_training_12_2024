from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id = 'hello_world',
    start_date = datetime.now() - timedelta(days=14),
    description = 'This DAG will print Hello and World'
    schedule = "@daily",
):

    hello = BashOperator(task_id = 'hello', bash_command = "echo 'hello'")
    world = PythonOperator(task_id = "world", python_callable = lambda: print("world"))

    hello >> world