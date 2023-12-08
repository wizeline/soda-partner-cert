import uuid
from typing import Literal, Optional

import requests
from dagster import ConfigurableResource
from soda.scan import Scan


class ScanError(Exception):
    """Error raised whenever a scan results with failed checks."""


class SodaScanResource(ConfigurableResource):
    """Soda resource to run CLI."""

    config_file: str
    checks_file: str
    data_source: str

    def scan(self, scan_definition: Optional[str] = None, is_local: bool = False):
        scan = self.get_scan(scan_definition)
        scan.set_is_local(is_local)

        exit_code = scan.execute()

        print(scan.get_logs_text())

        if exit_code != 0:
            raise ScanError("Scan finished with errors.")

        scan.assert_no_checks_fail()

        return exit_code

    def get_scan(self, scan_definition: Optional[str] = None):
        scan = Scan()
        scan.set_verbose()
        scan.set_scan_definition_name(scan_definition or str(uuid.uuid4()))
        scan.add_configuration_yaml_file(self.config_file)
        scan.set_data_source_name(self.data_source)
        scan.add_sodacl_yaml_file(self.checks_file)

        return scan


class SodaReportingResource(ConfigurableResource):
    """Soda resource to access reporting API"""

    api_key_id: str
    api_key_secret: str
    region: str

    @property
    def base_url(self) -> str:
        match self.region.upper():
            case "EU":
                return "https://reporting.cloud.soda.io/v1/"
            case "US":
                return "https://reporting.cloud.us.soda.io/v1/"
            case _:
                raise ValueError("Unknown region.")

    def datasets(self) -> dict:
        return self._make_api_call("/coverage/datasets")

    def datasets_health(self) -> dict:
        return self._make_api_call("/quality/dataset_health")

    def _make_api_call(self, endpoint: str) -> dict:
        url = self.base_url + endpoint.lstrip("/")
        response = requests.post(
            url=url,
            headers={
                "X-API-KEY-ID": self.api_key_id,
                "X-API-KEY-SECRET": self.api_key_secret,
            },
            timeout=60,
        )

        if response.status_code != 200:
            raise ValueError(
                f"Response code is not 200. Received: {response.status_code}"
            )

        return response.json()
