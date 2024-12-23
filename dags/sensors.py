from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.http.sensors.http import HttpSensor


with DAG(
    dag_id = 'sensors_exercise',
    start_date = datetime.now() - timedelta(days=20),
    schedule = "@daily",
):

    check_data = HttpSensor(task_id = 'check_data', http_conn_id = 'http_delayed', mode = 'reschedule', endpoint = '')

    run_something = PythonOperator(task_id = 'doing_stuff', python_callable = lambda: print('doing it for'))

    check_data >> run_something