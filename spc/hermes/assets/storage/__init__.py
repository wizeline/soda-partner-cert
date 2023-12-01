from dagster import asset

from spc.hermes.resources.kaggle import KaggleResource


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
