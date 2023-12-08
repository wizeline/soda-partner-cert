from dagster import asset

from spc.hermes.resources.kaggle import KaggleResource
from spc.hermes.resources.soda import SodaReportingResource


@asset(
    key_prefix=["kaggle"],
    group_name="ev_charging",
    io_manager_key="storage_io",
    compute_kind="python",
)
def flat_residential_ev_charging(kaggle: KaggleResource) -> bytes:
    """Binary file of residential EV charging reports zipped in an archive"""
    return kaggle.download_request(
        "anshtanwar", "residential-ev-chargingfrom-apartment-buildings"
    )


@asset(
    key_prefix=["soda"],
    group_name="data_quality",
    io_manager_key="storage_io",
    compute_kind="python",
)
def flat_dataset_coverage(soda_reporting: SodaReportingResource) -> dict:
    return soda_reporting.datasets()


@asset(
    key_prefix=["soda"],
    group_name="data_quality",
    io_manager_key="storage_io",
    compute_kind="python",
)
def flat_dataset_health(soda_reporting: SodaReportingResource) -> dict:
    return soda_reporting.datasets_health()
