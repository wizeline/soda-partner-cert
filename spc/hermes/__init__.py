from dagster import Definitions, EnvVar
from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

from . import assets, jobs
from .resources.kaggle import KaggleResource

defs = Definitions(
    assets=assets.get_assets(),
    resources={
        "kaggle": KaggleResource(
            username=EnvVar("KAGGLE_USERNAME"),
            password=EnvVar("KAGGLE_KEY"),
        ),
        "warehouse_pandas_io": DuckDBPandasIOManager(database="/tmp/athena.duck"),
        "dbt_optimus": DbtCliResource(
            profiles_dir="./",
            project_dir="./spc/optimus",
            target="local",
        ),
    },
    jobs=jobs.get_jobs(),
)
