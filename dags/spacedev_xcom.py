from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.taskinstance import TaskInstance as ti


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

    print('Number of launch is ', launches['count'], "from", input_path )


with DAG(
    dag_id="context_exercise_xcom",
    start_date=datetime.now() - timedelta(days=10),
    schedule_interval="@daily",
):

    echo_logical_date = BashOperator(task_id = 'print_logical_date', bash_command = "echo {{ ts }}")

    launch_data = PythonOperator(task_id = 'fetch_launch_data', python_callable = _download_launches, templates_dict = {"output_path": "/tmp/launches/2021-01-01.json",
            "window_start": "2021-01-01T00:00:00Z",
            "window_end": "2021-01-02T00:00:00Z",})

    launch_count = PythonOperator(task_id = 'count_launch', python_callable = _print_launch_count, templates_dict = ti.xcom_pull(task_ids='launch_data'))

    echo_logical_date >> launch_data >> launch_count
