"""Helper functions for the job."""

import logging
from typing import Any, List, Union, Dict
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import DataType

logger = logging.getLogger(__name__)


def get_spark() -> SparkSession:
    """Retrieve new sparksession.

    Returns:
        SparkSession: SparkSession Object
    """
    spark = SparkSession.builder.getOrCreate()

    return spark


def replace_missing(df: DataFrame, column_names: List[str], default: Any = 0) -> DataFrame:
    """Replace the `NaN` and `Null` values with the provided dafault.

    Args:
        df (DataFrame): Dataframe on which operation should be done
        column_names (List[str]): Subset of columns based on which null replacement to be done

    Returns:
        DataFrame: Modified dataframe
    """
    return df.na.fill(value=default, subset=column_names)


def convert_to_type(df: DataFrame, to_type: Union[str, DataType], column: str) -> DataFrame:
    """Cast provided column to the given Spark Type.

    Args:
        df (DataFrame): Dataframe on which casting should be done
        to_type (Union[str, DataType]): Target type to convert the column to (Type can be
                                    specified as valid `string` as well as as Spark `DataType`)
        column (str): column to be converted

    Returns:
        DataFrame: Type converted dataframe
    """
    return df.withColumn(column, col(column).cast(to_type))


def map_to_type(df: DataFrame, cast_map: Dict[str, Union[str, DataType]]) -> DataFrame:
    """Cast columns to the given Spark Type as per provided mapping.

    Args:
        df (DataFrame): Dataframe on which casting should be done
        cast_map (Dict[str, Union[str, DataType]]): Python Dictionary object with type mapping for columns

    Returns:
        DataFrame: Type converted dataframe
    """
    from functools import reduce

    df = reduce(
        lambda x, y: x.withColumn(y[0], col(y[0]).cast(y[1])),
        cast_map.items(),
        df,
    )

    return df
