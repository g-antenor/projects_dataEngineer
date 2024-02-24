import subprocess
from airflow import DAG
from docker.types import Mount
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.oprators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.docker.operators.docker import DockerOperator

CONN_ID = ''

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description="Um ELT workflow com dbt",
    start_date=datetime(2024, 2, 23),
    catchup=False
)

t1 = AirbyteTriggerSyncOperator(
    task_id = 'airbyte_postgres_postgres',
    python_callable = 'airbyte',
    connection_id = CONN_ID,
    asynchronous = False,
    timeout = 3600,
    wait_seconds = 3,
    dag = dag
)

t2 = DockerOperator(
    task_id = 'dbt_run',
    image = 'ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command = [
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt"
    ],
    auto_remove = True,
    docker_url = 'unix://var/run/docker.sock',
    network_mode = 'bridge',
    mounts = [
        Mount(source = '/Users/Nave/Documents/etl/custom_postgres', target = '/opt/dbt', type = 'bind'),
        Mount(source = '/Users/Nave/.dbt', target = '/root', type = 'bind')
    ],
    dag = dag
)

t1 >> t2






