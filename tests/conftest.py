import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session():
    session = SparkSession.builder.master("local[*]").getOrCreate()

    with session as spark:
        yield spark
