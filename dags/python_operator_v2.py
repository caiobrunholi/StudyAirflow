from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task
import pendulum
import pprint

with DAG(
    dag_id="python_operator_v1",
    schedule="* * * * *",
    start_date=pendulum.datetime(2023, 6, 22, 14, 10, tz="America/Sao_Paulo"),
    catchup=True,
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    @task(task_id="python")
    def meu_codigo(ds=None, **kwargs):
        pprint.pprint(kwargs)
        print(ds)
        return "Meu retorno agora é esse texto"

    python = meu_codigo()

start >> python >> end
