import json
from pathlib import Path

import airflow.utils.dates
import requests
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pprint import pprint


API_URL = "https://lldev.thespacedevs.com/2.3.0/launches"

with DAG(
    dag_id="exercise_templating",
    start_date=airflow.utils.dates.days_ago(7),
    schedule_interval="@daily",
) as dag:

    def print_context_func(**context):
        pprint(context)

    def _download_launches(**context):
        templates_dict = context["templates_dict"]
        output_path = Path(templates_dict["output_path"])
        own_stuff = templates_dict["own_stuff"]

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
        print_context_func(**context)

    def _print_launch_count(**context):
        input_path = context["templates_dict"]["input_path"]

        with Path(input_path).open() as file_:
            launches = json.load(file_)

        print(f"""Counted {launches["count"]} launches from {input_path}""")
        print_context_func(**context)

    print_date = BashOperator(
        task_id="print_date", bash_command="echo {{ logical_date }}"
    )

    download_launches = PythonOperator(
        task_id="download_launches",
        python_callable=_download_launches,
        templates_dict={
            "output_path": "/tmp/launches/{{ds}}.json",
            "window_start": "{{data_interval_start | ds}}T00:00:00Z",
            "window_end": "{{data_interval_end | ds}}T00:00:00Z",
            "own_stuff" : "this is my own"
        },
    )

    check_for_launches = PythonOperator(
        task_id="check_for_launches",
        python_callable=_print_launch_count,
        templates_dict={"input_path": "/tmp/launches/{{ds}}.json"},
    )

    print_date >> download_launches >> check_for_launches
