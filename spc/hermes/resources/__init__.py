from enum import Enum
from typing import Any, Union

from dagster import EnvVar, FilesystemIOManager
from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagster_gcp import GCSPickleIOManager, GCSResource
from dagster_gcp_pandas import BigQueryPandasIOManager

from .kaggle import KaggleResource
from .soda import SodaResource


class Environment(str, Enum):
    LOCAL = "local"
    DEV = "development"


def get_resources(
    environment: Union[Environment, str] = Environment.LOCAL
) -> dict[str, Any]:
    print("Building resources for specified environment:", environment)

    base_resources = {
        "kaggle": KaggleResource(
            username=EnvVar("KAGGLE_USERNAME"),
            password=EnvVar("KAGGLE_KEY"),
        ),
        "dbt_optimus": DbtCliResource(
            profiles_dir="./",
            project_dir="./spc/optimus",
            target=environment,
        ),
        "soda_": SodaResource(
            config_file="./spc/soda/configuration.yml",
            checks_file="./spc/soda/checks.yml",
            data_source="athena_local",
        ),
    }

    match environment:
        case Environment.LOCAL:
            return {
                **base_resources,
                "storage_io": FilesystemIOManager(base_dir="/tmp/poseidon"),
                "warehouse_pandas_io": DuckDBPandasIOManager(
                    database="/tmp/athena.duck"
                ),
            }
        case Environment.DEV:
            project = EnvVar("GCP_PROJECT")

            return {
                **base_resources,
                "storage_io": GCSPickleIOManager(
                    gcs=GCSResource(project=project),
                    gcs_bucket="enrique-o-cool-bucket",
                    gcs_prefix="poseidon",
                ),
                "warehouse_pandas_io": BigQueryPandasIOManager(
                    project=project,
                    temporary_gcs_bucket="enrique-o-cool-bucket",
                ),
            }
        case _:
            raise ValueError("Provided an unknown environment value.")
