# Apache Airflow

## Videos e Links

https://www.youtube.com/watch?v=9QQRvyqXlbQ

https://www.youtube.com/watch?v=VlLn-Fm4sws

https://www.youtube.com/playlist?list=PLFeyfVYazTkIahiXiL0ialpIEEOI70OgI

[Home](https://airflow.apache.org/)

## O que é

Plataforma pra programar e executar tarefas automatizadas → **Workflows**

- Os pipelines são criados em código (Python)
    - Os pipelines usam o Jinja
- É escalável
- Ele é extremamente modular, então a instalação padrão vem somente com os componentes principais
    - Se precisar integrar o Airflow com tecnologias externas é preciso usar os **Providers**

## DAG

Direct Acyclic Graph

Gráficos de representação de tarefas (fluxos de trabalho)

![image.png](Apache%20Airflow%201734b7f58b9d807cade9cf681555e2d4/image.png)

Não são cíclicas

![image.png](Apache%20Airflow%201734b7f58b9d807cade9cf681555e2d4/image%201.png)

## Quando não é recomendado

- Ele não é recomendado para soluções que façam streaming de dados
- Espera que o fluxo de trabalho seja estável ou com poucas mudanças

## Componentes

### Scheduler

Responsável pelo agendamento das DAGs e envio das tarefas para os workers

- Workflows podem ser iniciados por tempo ou por gatilhos externos (trigger)

![image.png](Apache%20Airflow%201734b7f58b9d807cade9cf681555e2d4/image%202.png)

- Garante a ordem de execução de tarefas e que tasks dependentes sejam executadas somente após da conclusão das anteriores
- Possui configuração de retries
- Gerencia concorrência de recursos

### Executer

Responsável pela execução das tarefas que encaminha as tarefas para os workers

- Determina como e onde as tarefas serão executadas
    - Processos locais
    - Threads
    - Sistemas de Cluster distribuído

Tipos de executores

- Sequential Executer
    - Executor padrão
    - Tarefas são executadas sequencialemente de forma local (dev e debug)
- Local Executer
    - Tarefas em paralelo com processos locais
    - Instâncias menores do Airflow
- Celery Executer
    - Distribuição e execução de tarefas paralelas em múltiplas máquinas utilizando o Celery
        - Celery: Sistema de filas de tarefas distribuídas
    - Adequado para instâncias maiores do Airflow → Execução em múltiplos servidores
- Kubernetes Executer
    - Lança cada tarefa em seu próprio Pod Kubernetes
    - Execução distribuída de tarefas utilizando os recursos de orquestração do Kubernetes

### Web Server

Interface web para o usuário interagir com as DAGs e as Tasks

### DAGs Folder

Pasta com as DAGs onde são armazenados os códigos Pyhton

### Metadados (Metastore)

Banco de dados que cumpre papel de repositório da ferramenta, utilizado pelo Scheduler e pelo Executer para armazenar os estados das execuções.

- Armazena o histórico de execução e se foram bem sucedidas ou não
- Permite que o scheduler organize retries
- Configurações como variáveis de banco de dados

![image.png](Apache%20Airflow%201734b7f58b9d807cade9cf681555e2d4/image%203.png)

### Operators

Determinam exatamente o que acontece quando uma tarefa é executada dentro de uma DAG

- Sensors Operators
    - Sensores
    - Tipos especiais de operadores que pausa o fluxo de uma operação até que uma condição especial seja atendida
        - Escutam estados externos (ex: HTTPSensor → pausa a execução até que uma resposta HTTP seja verificada)
- Transfer Operators
    - Usados para mover dados de um lugar para outro
    - Ex: S3toRedshiftOperador → move dados de um Bucket S3 para uma tabela Amazon Redsift
- Action Operators
    - Executam uma ação ou tarefa específica
        - Executar um script ou consulta SQL
    - Ex: BashOperator → Operador de ação que executa um comando bash
    

## Providers

Pacotes que extendem o Airflow para se conectar e interagir com sistemas externos

Ex: para usar o Apache Spark é preciso usar o provedor da Databricks

Os pacotes são instalados usando o comando:

```bash
pip install apache-aiflow-providers-databricks
```

## Desenvolvimento

### Schedule

Intervalo entre execuções e data de início

```python
with DAG('tutorial_dag', start_date = datetime (2021,12,1),
          schedule interval '30 * * * *', catchup= False) as dag:
```

O intervalo é determinado utilizando a mesma anotação de agendamento que o crontab

A primeira execução sempre será em `datetime + schedule_interval`

### Criação de DAGs

Existe mais de uma forma de escrever DAGs:

```python
"""
Primeira DAG: Hello World
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="a_primeira_DAG_v0",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    doc_md=__doc__,
):
    start = EmptyOperator(task_id="start")
    hello = BashOperator(task_id="hello", bash_command="echo hello world")
    end = EmptyOperator(task_id="end")

(start >> hello >> end)

```

```python
"""
Primeira DAG: Hello World
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

minha_dag = DAG(
    dag_id="a_primeira_DAG_v1",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    doc_md=__doc__,
)
start = EmptyOperator(task_id="start", dag=minha_dag)
hello = BashOperator(task_id="hello", bash_command="echo hello world", dag=minha_dag)
end = EmptyOperator(task_id="end", dag=minha_dag)

start >> hello >> end

```

```python
"""
Primeira DAG: Hello World
"""

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id="a_primeira_DAG_v2",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    doc_md=__doc__,
)
def a_primeira_DAG_v2():
    start = EmptyOperator(task_id="start")
    hello = BashOperator(task_id="hello", bash_command="echo hello world")
    end = EmptyOperator(task_id="end")
    start >> hello >> end

criar_DAG = a_primeira_DAG_v2()

```