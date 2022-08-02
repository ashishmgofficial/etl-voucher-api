"""The main Executor pipeline for the job."""

from dataclasses import dataclass
from etl.customer.factory import CustomerDomain
from pyspark.sql import SparkSession, DataFrame


@dataclass
class Executor:
    """Executor Class for the ETL job.

    Args:
        domain (str): The data domain
        dataset (str): The dataset within the domain
        raw_path (str): Raw basepath location for ETL jobs
        output_path (str): Processed basepath localtion for ETL Jobs
    """

    domain: str
    dataset: str
    raw_path: str
    output_path: str

    def _read_source_data(self, session: SparkSession) -> DataFrame:
        df = session.read.format("parquet").option("mergeSchema", True).load(self.raw_path)
        return df

    def _write_to_target(self, df: DataFrame) -> None:
        df.coalesce(1).write.format("csv").option("header", True).mode("overwrite").save(self.output_path)

    def _get_domain_provider(self):
        if self.domain.lower() == "customer":
            return CustomerDomain(self.dataset)

    def run(self, session: SparkSession) -> None:
        """The main driver method for the job.

        Args:
            session (SparkSession): Spark session object.
        """
        domain_provider = self._get_domain_provider()
        processor = domain_provider.get_processor()
        raw_df = self._read_source_data(session)
        processed_df = processor.process(raw_df)
        self._write_to_target(processed_df)
