"""Main module for the Job."""

import argparse

from etl.executor import Executor
from pathlib import Path
import etl.enums as constants
from etl.helpers import get_spark


def resolve_args():  # pragma: no cover
    """Resolves the CLI Arguments.

    Returns:
        Namespace: An argparse namespace object.
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-D",
        "--domain",
        required=True,
        type=str,
        help="Data Domain",
        choices=constants.Domain.get_registered_domains(),
    )
    argparser.add_argument("-d", "--dataset", required=True, type=str, help="Dataset within domain")
    argparser.add_argument(
        "-r", "--raw-basepath", required=True, type=Path, help="Basepath location of the raw data"
    )
    argparser.add_argument(
        "-t", "--processed-basepath", required=True, type=Path, help="Basepath location of the Processed data"
    )
    args = argparser.parse_args()

    return args


def main():  # pragma: no cover
    """Main method."""
    args = resolve_args()
    domain = args.domain
    dataset = args.dataset
    raw_path = f"{args.raw_basepath}/{domain}/{dataset}"
    target_path = f"{args.processed_basepath}/{domain}/{dataset}"
    executor = Executor(domain, dataset, raw_path, target_path)
    spark = get_spark()
    with spark:
        executor.run(spark)


if __name__ == "__main__":
    main()
