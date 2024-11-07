from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from breweries.scripts.bronze_script import run_bronze_script
from breweries.scripts.silver_script import run_silver_script
from breweries.scripts.gold_script import run_gold_script
from breweries.scripts.data_validation import FileNotEmptySensor
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import logging

BRONZE_FILE_PATH = os.path.join("data", "bronze", "raw_data.json")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    "breweries_pipeline",
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
    ) as dag:

    def log_success(**context):
        date = context['execution_date']
        logger = logging.getLogger("airflow.task")
        logger.info(f"Pipeline ran successfully on: {date}")


    create_bronze_layer = PythonOperator(
        task_id='create_bronze_layer',
        python_callable=run_bronze_script
    )

    check_if_bronze_is_empty = FileNotEmptySensor(
        task_id='check_if_bronze_is_empty',
        filepath=BRONZE_FILE_PATH
    )

    create_silver_layer = PythonOperator(
        task_id='create_silver_layer',
        python_callable=run_silver_script
    )

    create_gold_layer = PythonOperator(
        task_id='create_gold_layer',
        python_callable=run_gold_script
    )

    log_success_task = PythonOperator(
        task_id='log_success',
        python_callable=log_success,
        provide_context=True
    )


    create_bronze_layer >> check_if_bronze_is_empty >> create_silver_layer >> create_gold_layer >> log_success_task