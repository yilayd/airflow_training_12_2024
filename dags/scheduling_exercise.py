from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id = 'launch_rocket_scheduler',
    start_date = datetime.now() - timedelta(days=90),
    description = "Empty operators",
    schedule = '45 13 * * 2,4,6',
):

    rocket_material = EmptyOperator(task_id = 'procure_rocket_material') 
    fuel = EmptyOperator(task_id = 'procure_fuel') 

    stages  = [EmptyOperator(task_id = f"building_stage_{i}") for i in range(1,4)]
    
    launch = EmptyOperator(task_id = 'launching')

    rocket_material >> stages >> launch

    fuel >> stages[-1] >> launch

