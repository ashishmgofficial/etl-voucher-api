from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import pendulum
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import dag


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

    prepare_warehouse = PostgresOperator(task_id="setup_datawarehouse", sql="sql/customer/administrative.sql")

    load_to_warehouse = PostgresOperator(
        task_id="load_to_dw", sql="sql/customer/data_load_voucher_segmentation.sql"
    )

    generate_segmentation_views = PostgresOperator(
        task_id="generate_segment_views", sql="sql/customer/model_voucher_segmentation.sql"
    )

    sleep >> prepare_warehouse >> load_to_warehouse >> generate_segmentation_views


dag = etl_customer_voucher_assignment()
