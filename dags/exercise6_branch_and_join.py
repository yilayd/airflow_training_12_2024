from airflow import utils
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator


def _get_weekday(logical_date, **context):
    return logical_date.strftime("%a")  # “Mon”


with DAG(
    dag_id="branch_python_operator_example",
    start_date=utils.dates.days_ago(14),
    schedule="@daily",
):

    do_something = EmptyOperator(
        task_id="do_something",
    )

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    branching = BranchPythonOperator(
        task_id="branching",
        python_callable=_get_weekday,
    )

    do_something >> branching

    
    daily_tasks = [EmptyOperator(task_id=f"{day}") for day in days]    
         
    next_task = EmptyOperator(task_id='next', trigger_rule = 'none_failed_min_one_success')
    branching >> daily_tasks >> next_task 
