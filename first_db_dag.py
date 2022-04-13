from datetime import datetime

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

with DAG(
        dag_id='spline_databricks_operator',
        schedule_interval='@daily',
        start_date=datetime(2021, 1, 1),
        tags=['example'],
        catchup=False, ) as dag:
    task_params = {
        'existing_cluster_id': '',
        'notebook_task': {
            'notebook_path': '/Users/airflow@example.com/PrepareData',
        },
    }

    spline_databricks_job = DatabricksSubmitRunOperator(task_id='spline_job', json=task_params)

spline_databricks_job
