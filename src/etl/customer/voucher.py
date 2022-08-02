"""Module for Voucher data processing."""

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Any, Dict, List
from pyspark.sql import DataFrame
from pyspark.sql.types import *

from etl.helpers import replace_missing, map_to_type
import pyspark.sql.functions as F


FREQUENCY_SEGMENT = {"0-4": (0, 4), "5-13": (5, 13), "14-37": (14, 37)}
RECENCY_SEGMENT = {"30-60": (30, 60), "61-90": (61, 90), "91-120": (91, 120), "121-180": (121, 180)}


class SEGMENT(Enum):
    """Segments Enum."""

    FREQUENCY = 'frequency_segment'
    RECENCY = 'recency_segment'

    def get_variants(self) -> Dict[str, Any]:
        """Returns all the sub variants for the segments."""
        if self.value == 'frequency_segment':
            return FREQUENCY_SEGMENT
        return RECENCY_SEGMENT


VOUCHER_TYPE_MAPPING = {
    "total_orders": IntegerType(),
    "voucher_amount": IntegerType(),
    "timestamp": TimestampType(),
    "last_order_ts": TimestampType(),
    "first_order_ts": TimestampType(),
}


@dataclass
class VoucherProcessor:
    """Voucher processor class."""

    def _filter_invalid_orders(self, df: DataFrame) -> DataFrame:
        return df.filter("total_orders <> '' and total_orders <> '0.0'").filter("total_orders is not null")

    def __format_timestamp(self, df: DataFrame, columns: List[str]) -> DataFrame:
        return reduce(
            lambda x, y: x.withColumn(y, F.to_timestamp(F.col(y), "yyyy-MM-dd HH:mm:SS")), columns, df
        )

    def _segmentation_helper(
        self, df: DataFrame, segment: SEGMENT, column: str, event_timestamp_col: str = None
    ) -> DataFrame:

        if segment == SEGMENT.FREQUENCY:
            expr = reduce(
                lambda x, y: x.when(F.col(column).between(y[1][0], y[1][1]), y[0]),
                segment.get_variants().items(),
                F,
            )
        elif segment == SEGMENT.RECENCY:
            expr = reduce(
                lambda x, y: x.when(
                    F.datediff(F.col(event_timestamp_col), F.col(column)).between(
                        F.lit(y[1][0]), F.lit(y[1][1])
                    ),
                    y[0],
                ),
                segment.get_variants().items(),
                F,
            )
            expr = expr.when(F.datediff(F.col(event_timestamp_col), F.col(column)) >= 180, "180+")

        return df.withColumn(segment.value, expr)

    def pre_process(self, df: DataFrame) -> DataFrame:
        """Perform `preprocessing` for Voucher Assignment dataset.

        Args:
            df (DataFrame): Raw dataframe to process

        Returns:
            DataFrame: Processed Dataframe.
        """
        valid_orders_df = self._filter_invalid_orders(df)
        null_replaced_voucher_amounts_df = replace_missing(valid_orders_df, ["voucher_amount"], 0)
        type_corrected_df = map_to_type(null_replaced_voucher_amounts_df, VOUCHER_TYPE_MAPPING)
        type_corrected_df = type_corrected_df.filter("last_order_ts <= timestamp").filter(
            "last_order_ts >= first_order_ts"
        )

        deduplicated_df = type_corrected_df.drop_duplicates()
        return deduplicated_df

    def transform(self, df: DataFrame) -> DataFrame:
        """Apply defined transformations on the voucher dataset.

        Args:
            df (DataFrame): The cleaned Dataframe.

        Returns:
            DataFrame: Transformed Dataframe.
        """
        frequency_segmented_df = self._segmentation_helper(df, SEGMENT.FREQUENCY, "total_orders")
        recency_segmented_df = self._segmentation_helper(
            frequency_segmented_df, SEGMENT.RECENCY, "last_order_ts", "timestamp"
        )
        return recency_segmented_df

    def process(self, raw_df: DataFrame) -> DataFrame:
        """Main runner for the voucher processing.

        Args:
            raw_df (DataFrame): The Raw source Dataframe.

        Returns:
            DataFrame: Processed Dataframe.
        """
        clean_df = self.pre_process(raw_df)
        transformed_df = self.transform(clean_df)
        return transformed_df
