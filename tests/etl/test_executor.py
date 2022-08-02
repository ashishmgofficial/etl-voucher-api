from etl.executor import Executor
from etl.customer.factory import CustomerDomain
import pathlib
from pyspark.sql import SparkSession

RESOURCE_PATH = pathlib.Path(__file__).parent.absolute()

executor = Executor(
    "customer",
    "voucher",
    f"{RESOURCE_PATH}/resources/raw/customer/voucher",
    f"{RESOURCE_PATH}/resources/processed/customer/voucher",
)


def test_read_source_data(spark_session):
    source_df = executor._read_source_data(spark_session)
    assert source_df.count() == 511427


def test_get_domain_provider():
    assert isinstance(executor._get_domain_provider(), CustomerDomain) == True


def test_run(spark_session: SparkSession):
    executor.run(spark_session)
    df = spark_session.read.format("csv").option("header", True).load(f"{executor.output_path}/*.csv")
    assert df.count() == 379599
    extra_columns = ["frequency_segment", "recency_segment"]
    for column in extra_columns:
        assert column in df.columns
