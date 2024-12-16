
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pprint import pprint

def print_context_func(**context):
    pprint(context)


my_dag = DAG(
    dag_id="context_print",
    start_date=datetime.now() - timedelta(days=4),
    schedule_interval="@daily",
    tags=["exercise"],
)

    
print_context = PythonOperator(
    task_id="print_context",
    python_callable=print_context_func, dag = my_dag, op_kwargs = [1,2,3,4]
)