from dataclasses import dataclass
from etl.customer.factory import CustomerDomain
from etl.helpers import get_spark
from pyspark.sql import SparkSession, DataFrame


@dataclass
class Executor:
    domain: str
    dataset: str
    raw_path: str
    output_path: str

    def _read_source_data(self, session: SparkSession) -> DataFrame:
        df = session.read.format("parquet").option("mergeSchema", True).load(self.raw_path)
        return df

    def _write_to_target(self, df: DataFrame) -> None:
        df.write.format("csv").option("header", True).mode("append").save(self.output_path)

    def get_domain_provider(self):
        if self.domain.lower() == "customer":
            return CustomerDomain(self.dataset)

    def run(self):
        session = get_spark()
        domain_provider = self.get_domain_provider()
        processor = domain_provider.get_processor()
        raw_df = self._read_source_data(session)
        processed_df = processor.process(raw_df)
        self._write_to_target(processed_df)
        session.stop()
