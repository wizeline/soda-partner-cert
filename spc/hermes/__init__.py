import os

from dagster import Definitions

from . import assets, jobs, resources

environment = os.getenv("HERMES_ENVIRONMENT", "local")

defs = Definitions(
    assets=assets.get_assets(),
    resources=resources.get_resources(environment),
    jobs=jobs.get_jobs(),
)
