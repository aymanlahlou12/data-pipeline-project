from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'achille',
    'depends_on_past': False,
    'start_date': datetime(2026, 10, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_automated_pipeline',
    default_args=default_args,
    description='End-to-end daily weather ETL pipeline',
    schedule_interval='@daily', # Runs once a day automatically
    catchup=False
) as dag:

    extract_task = BashOperator(
        task_id='extract_api_data',
        bash_command='python /opt/airflow/scripts/extract_api.py'
    )

    load_staging_task = BashOperator(
        task_id='load_to_staging',
        bash_command='python /opt/airflow/scripts/load_to_staging.py'
    )

    transform_spark_task = BashOperator(
        task_id='transform_with_spark',
        bash_command='python /opt/airflow/scripts/transform_spark.py'
    )

    extract_task >> load_staging_task >> transform_spark_task