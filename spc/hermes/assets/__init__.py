from dagster import AssetExecutionContext, load_assets_from_package_module
from dagster_dbt import DbtCliResource, KeyPrefixDagsterDbtTranslator, dbt_assets

from . import storage, warehouse


@dbt_assets(
    manifest="./spc/optimus/target/manifest.json",
    dagster_dbt_translator=KeyPrefixDagsterDbtTranslator(
        asset_key_prefix=["warehouse"],
    ),
    name="analytics",
)
def analytics_assets(context: AssetExecutionContext, dbt_optimus: DbtCliResource):
    yield from dbt_optimus.cli(
        ["build"],
        context=context,
    ).stream()


def get_assets():
    return [
        *load_assets_from_package_module(storage, key_prefix=["storage"]),
        *load_assets_from_package_module(warehouse, key_prefix=["warehouse"]),
        analytics_assets,
    ]
