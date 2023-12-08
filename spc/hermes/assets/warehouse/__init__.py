from io import BytesIO
from zipfile import ZipFile

import pandas
from dagster import asset
from pandas import DataFrame as PandasDF


def _load_archived_df(archive_bytes: bytes, filename: str) -> PandasDF:
    archive = BytesIO(archive_bytes)
    with ZipFile(file=archive, mode="r") as flat:
        with flat.open(filename) as raw:
            df = pandas.read_csv(raw, sep=";", header=0, na_values="NA")

    return df


@asset(
    key_prefix=["kaggle"],
    group_name="ev_charging",
    io_manager_key="warehouse_pandas_io",
    compute_kind="pandas",
)
def raw_ev_charging_reports(flat_residential_ev_charging: bytes) -> PandasDF:
    """Raw extract of EV charging reports as Dataframe"""
    return _load_archived_df(
        flat_residential_ev_charging,
        "archive (34)/Dataset 1_EV charging reports.csv",
    )


@asset(
    key_prefix=["kaggle"],
    group_name="ev_charging",
    io_manager_key="warehouse_pandas_io",
    compute_kind="pandas",
)
def raw_hourly_ev_loads(flat_residential_ev_charging: bytes) -> PandasDF:
    """Raw extract of hourly EV loads as Dataframe"""
    return _load_archived_df(
        flat_residential_ev_charging,
        "archive (34)/Dataset 2_Hourly EV loads - Per user.csv",
    )


@asset(
    key_prefix=["soda"],
    group_name="data_quality",
    io_manager_key="warehouse_pandas_io",
    compute_kind="pandas",
)
def dataset_coverage(flat_dataset_coverage: dict) -> PandasDF:
    return PandasDF.from_records(flat_dataset_coverage["data"])


@asset(
    key_prefix=["soda"],
    group_name="data_quality",
    io_manager_key="warehouse_pandas_io",
    compute_kind="pandas",
)
def dataset_health(flat_dataset_health: dict) -> PandasDF:
    return PandasDF.from_records(flat_dataset_health["data"])
