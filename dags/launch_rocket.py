from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id = 'launch_rocket',
    start_date = datetime.now() - timedelta(days=3),
    description = "Empty operators",
    schedule = '@daily',
):

    procure_rocket_material = EmptyOperator(task_id = 'rocket_material_is_procured') 
    
    procure_fuel = EmptyOperator(task_id = 'rocket_is_fueled') 

    build_stage_1 = EmptyOperator(task_id = 'building_stage_1') 

    build_stage_2 = EmptyOperator(task_id = 'building_stage_2') 

    build_stage_3 = EmptyOperator(task_id = 'building_stage_3') 

    launch = EmptyOperator(task_id = 'launching')


    procure_rocket_material >> [build_stage_1, build_stage_2, build_stage_3] >> launch

    procure_fuel >> build_stage_3 >> launch

