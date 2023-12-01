import uuid
from typing import Optional

from dagster import ConfigurableResource, OpExecutionContext
from soda.scan import Scan


class ScanError(Exception):
    """Error raised whenever a scan results with failed checks."""


class SodaResource(ConfigurableResource):
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
