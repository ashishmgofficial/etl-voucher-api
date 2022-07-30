"""Helper functions for the job."""

import logging
from pyspark.sql import SparkSession


logger = logging.getLogger(__name__)


def get_spark() -> SparkSession:
    """Retrieve new sparksession.

    Returns:
        SparkSession: SparkSession Object
    """

    spark = SparkSession.builder.getOrCreate()

    return spark
