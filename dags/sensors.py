from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import airflow.providers.http.sensors.http


with DAG(
    dag_id = 'sensors_exercise',
    start_date = datetime.now() - timedelta(days=20),
    schedule = "@daily",
):

    check_data = HttpSensor(http_conn_id = 'http_delayed', mode = 'reschedule', extra_options = {'check_response': 20000})

    run_something = PythonOperator(task_id = 'doing_stuff', python_callable = lambda x: print('doing it for', {{ ts }}))

    check_data >> run_something