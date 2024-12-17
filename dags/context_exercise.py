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
    output_path = Path(templates_dict["output_path"])

    response = requests.get(
        API_URL,
        params={
            "window_start__gte": templates_dict["window_start"],
            "window_end__lt": templates_dict["window_end"],
        },
    )
    response.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as file_:
        json.dump(response.json(), file_)


def _print_launch_count(**context):
    # TODO: Finish this task. Should load the launch JSON file
    # and print the 'count' field from it's contents.

    input_path = context['templates_dict']['input_path']

    with input_path.open("w") as file_:
        launches = json.load(file_)

    print('Number of launch is ', launches['count'], "from", input_path )

def print_context_func(numbers, **context):
    print(numbers[0])
    pprint(context)

with DAG(
    dag_id="context_exercise",
    start_date=airflow.utils.dates.days_ago(7),
    schedule_interval="@daily",
):

    echo_logical_date = BashOperator(task_id = 'print_logical_date', bash_command = "echo {{ ts }}")

    launch_data = PythonOperator(task_id = 'fetch_launch_data', python_callable = _download_launches, templates_dict = {"output_path": "/tmp/launches/2021-01-01.json",
            "window_start": "2021-01-01T00:00:00Z",
            "window_end": "2021-01-02T00:00:00Z",})

    launch_count = PythonOperator(task_id = 'count_launch', python_callable = _print_launch_count, templates_dict = {"input_path": "/tmp/launches/2021-01-02.json"})
    print_context = PythonOperator(
        task_id="print_context",
        python_callable=print_context_func, dag = my_dag, op_kwargs = {'numbers':[1,2,3,4]}
)
    echo_logical_date >> launch_data >> launch_count >> print_context
