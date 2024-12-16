from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


def some_function():

    print("This is inside of a python function")
    print("done!")

with DAG(
    dag_id = 'launch_rocket',
    start_date = datetime.now() - timedelta(days=3),
    description = "Empty operators",
    schedule = '@daily',
):

    procure_rocket_material = EmptyOperator(task_id = 'rocket_material_is_procured') 

    python = PythonOperator(task_id = 'python1', python_callable = some_function)

    python2  = [PythonOperator(task_id = f"python{i}", python_callable = lambda: print(i) ) for i in range(2,10,2)]
    procure_fuel = EmptyOperator(task_id = 'rocket_is_fueled') 

    build_stage_1 = EmptyOperator(task_id = 'building_stage_1') 

    build_stage_2 = EmptyOperator(task_id = 'building_stage_2') 

    build_stage_3 = EmptyOperator(task_id = 'building_stage_3') 

    launch = EmptyOperator(task_id = 'launching')


    procure_rocket_material >> [build_stage_1, build_stage_2, build_stage_3] >> launch

    procure_fuel >> build_stage_3 >> launch >> python >> python2

