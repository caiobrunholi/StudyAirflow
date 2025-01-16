from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(
    dag_id="_dag_xcom_2",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 4, 1, tz="UTC"),
    catchup=False
) as dag:
    start = EmptyOperator(
        task_id="start",
    )
    coleta_valor_3 = BashOperator(
        task_id="coleta_valor_3",
        bash_command="echo 'retorno capturado: {{ti.xcom_pull(dag_id = '_dag_xcom',task_ids='executa_algo_3')}}'",
        do_xcom_push=False
    )

start >> coleta_valor_3
