from dagster import asset

from spc.hermes.resources.kaggle import KaggleResource


@asset(group_name="kaggle", compute_kind="python")
def flat_residential_ev_charging(kaggle: KaggleResource) -> bytes:
    return kaggle.download_request(
        "anshtanwar", "residential-ev-chargingfrom-apartment-buildings"
    )
