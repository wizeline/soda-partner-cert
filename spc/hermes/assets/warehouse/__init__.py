from io import BytesIO
from zipfile import ZipFile

import pandas
from dagster import asset
from pandas import DataFrame as PandasDF


def load_archived_df(archive_bytes: bytes, filename: str) -> PandasDF:
    archive = BytesIO(archive_bytes)
    with ZipFile(file=archive, mode="r") as flat:
        with flat.open(filename) as raw:
            df = pandas.read_csv(raw, sep=";", header=0, na_values="NA")

    return df


@asset(io_manager_key="warehouse_pandas_io", group_name="kaggle", compute_kind="pandas")
def raw_ev_charging_reports(flat_residential_ev_charging: bytes) -> PandasDF:
    return load_archived_df(
        flat_residential_ev_charging,
        "archive (34)/Dataset 1_EV charging reports.csv",
    )


@asset(io_manager_key="warehouse_pandas_io", group_name="kaggle", compute_kind="pandas")
def raw_hourly_ev_loads(flat_residential_ev_charging: bytes) -> PandasDF:
    return load_archived_df(
        flat_residential_ev_charging,
        "archive (34)/Dataset 2_Hourly EV loads - Per user.csv",
    )
