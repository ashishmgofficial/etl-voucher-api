from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import pendulum
from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task


@dag(
    schedule_interval='@once',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['dh'],
)
def etl_customer_voucher_assignment():
    args = [
        "--domain",
        "customer",
        "--dataset",
        "voucher",
        "--raw-basepath",
        "/opt/application/data/raw",
        "--processed-basepath",
        "/opt/application/data/processed",
    ]
    sleep = BashOperator(task_id='sleep', bash_command='sleep 10')
    etl_task = SparkSubmitOperator(
        task_id="spark_etl", application="local:///opt/application/src/etl/main.py", application_args=args
    )

    sleep >> etl_task


dag = etl_customer_voucher_assignment()
