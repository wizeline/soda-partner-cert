import os
import tempfile
from typing import Generator, TypeVar

import duckdb
import pytest
import yaml

from spc.hermes.resources.soda import SodaResource

Yield = Generator[TypeVar("T"), None, None]
TEST_DB_PATH = "/tmp/test.duck"
TEST_DATA_SOURCE = "test_db"


@pytest.fixture()
def database():
    with duckdb.connect(TEST_DB_PATH) as duck:
        duck.sql(
            "create table if not exists sample_table as (select 'num' as key, "
            "42 as val)"
        )

    yield TEST_DB_PATH

    os.remove(TEST_DB_PATH)


@pytest.fixture()
def config_filename() -> Yield[str]:
    config = {
        f"data_source {TEST_DATA_SOURCE}": {
            "type": "duckdb",
            "database": TEST_DB_PATH,
            "read_only": True,
        },
        "soda_cloud": {
            "host": "cloud.us.soda.io",
            "api_key_id": os.getenv("SODA_CLOUD_API_KEY_ID"),
            "api_key_secret": os.getenv("SODA_CLOUD_API_KEY_SECRET"),
        },
    }

    with tempfile.NamedTemporaryFile("+r", encoding="UTF-8") as tmp:
        yaml.dump(config, tmp)
        tmp.flush()

        yield tmp.name


@pytest.fixture()
def checks_filename() -> Yield[str]:
    checks = {
        "checks for sample_table": [
            {"row_count > 0": {"name": "Non-empty"}},
            {
                "invalid_count(val) = 0": {
                    "name": "Invalid values",
                    "valid values": [42],
                }
            },
        ]
    }

    with tempfile.NamedTemporaryFile("+r", encoding="UTF-8") as tmp:
        yaml.dump(checks, tmp)
        tmp.flush()

        yield tmp.name


@pytest.fixture()
def resource(
    config_filename: str, checks_filename: str, database: str
) -> Yield[SodaResource]:
    print("Creating test db in path:", database)
    _r = SodaResource(
        config_file=config_filename,
        checks_file=checks_filename,
        data_source=TEST_DATA_SOURCE,
    )

    yield _r


def test_soda_resource_scan(resource: SodaResource):
    resource.scan(is_local=True)
