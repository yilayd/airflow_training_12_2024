import json
from pathlib import Path

import airflow.utils.dates
import requests
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


API_URL = "https://lldev.thespacedevs.com/2.3.0/launches"

def _download_launches(**context):
    templates_dict = context["templates_dict"]
    
    response = requests.get(
        API_URL,
        params={
            "window_start__gte": templates_dict["date_interval_start"],
            "window_end__lt": templates_dict["date_interval_end"],
        },
    )
    response.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as file_:
        json.dump(response.json(), file_)

    output_path = Path(templates_dict["output_path"])

def _print_launch_count(**context):
    # TODO: Finish this task. Should load the launch JSON file
    # and print the 'count' field from it's contents.

    output = context['templates_dict']['output_path']

    print('Number of launch is ', output['count'])


with DAG(
    dag_id="context_exercise",
    start_date=airflow.utils.dates.days_ago(7),
    schedule_interval="@daily",
):

    echo_logical_date = BashOperator(task_id = 'print_logical_date', bash_command = "echo {{ ts }}")

    launch_data = PythonOperator(task_id = 'fetch_launch_data', python_callable = _download_launches)

    launch_count = PythonOperator(task_id = 'count_launch', python_callable = _print_launch_count)

    echo_logical_date >> launch_data >> launch_count
