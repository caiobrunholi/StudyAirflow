from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import pendulum
import numpy as np

def gera_numero_1(ti):
    numero = np.random.randint(1, 10)
    ti.xcom_push(key="random_number", value=numero)
    return 0

def gera_numero_2():
    numero = np.random.randint(1, 10)
    return numero

with DAG(
    dag_id="_dag_xcom_",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 4, 1, tz="UTC"),
    catchup=False
) as dag:
    start = EmptyOperator(
        task_id="start",
    )
    executa_algo = PythonOperator(task_id="executa_algo", python_callable=gera_numero_1)
    executa_algo_2 = PythonOperator(
        task_id="executa_algo_2", python_callable=gera_numero_2
    )
    executa_algo_3 = BashOperator(
        task_id="executa_algo_3",
        bash_command='echo "Xcom"',
        do_xcom_push=True,
    )
    coleta_valor_1 = BashOperator(
        task_id="coleta_valor_1",
        bash_command="echo 'retorno caoturado: {{ti.xcom_pull(key='rando_number')}}'"
    )
    coleta_valor_2 = BashOperator(
        task_id="coleta_valor_2",
        bash_command="echo 'retorno capturado: {{ti.xcom_pull(task_ids=['executa_algo_2'])}}'"
    )
    coleta_valor_3 = BashOperator(
        task_id="coleta_valor_3",
        bash_command="echo 'retorno capturado: {{ti.xcom_pull(task_ids=['executa_algo_3'])}}'",
        do_xcom_push=False
    )
    
start >> executa_algo >> coleta_valor_1
start >> executa_algo_2 >> coleta_valor_2
start >> executa_algo_3 >> coleta_valor_3
