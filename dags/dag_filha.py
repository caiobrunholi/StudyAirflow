"""
DAG Principal
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
import pendulum
import pprint
import datetime


def print_filha(**kwargs):
    print("DAG filha")
    pprint.pprint(kwargs)
    return "filha"


with DAG(
    dag_id="DAG_filha",
    schedule="0 18 * * *",
    start_date=pendulum.datetime(2023, 6, 20, tz="America/Sao_Paulo"),
    catchup=True,
) as dag:
    start = EmptyOperator(task_id="start")
    wait_principal = ExternalTaskSensor(
        task_id="wait_principal",
        external_dag_id="DAG_principal",
        external_task_id="python_principal",
        execution_delta=datetime.timedelta(hours=1),
        poke_interval=30,
        mode="reschedule",
    )
    end = EmptyOperator(task_id="end")
