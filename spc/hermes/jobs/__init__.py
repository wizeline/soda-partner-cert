from dagster import AssetSelection, define_asset_job, job, op

from spc.hermes.resources.soda import SodaResource

EV_CHARGING_ETL = define_asset_job(
    name="ev_charging_etl",
    selection=AssetSelection.groups("ev_charging")
    | (
        AssetSelection.groups("ev_charging").downstream()
        & AssetSelection.groups("analytics")
    ),
)


@op
def run_soda_scan(soda_: SodaResource):
    scan = soda_.get_scan()
    _ec = scan.execute()

    if _ec != 0:
        raise RuntimeError("Error during scan execution. Exit code is not 0.")


@job
def ev_charging_scan():
    run_soda_scan()


def get_jobs():
    return [EV_CHARGING_ETL, ev_charging_scan]
