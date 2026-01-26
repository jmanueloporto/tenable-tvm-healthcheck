"""
Scanner Infrastructure Audit Module
Version: 2.0.0
Description: Monitors and audits the health of Tenable.io sensors (scanners).
"""
import re

class ScannerHealthModule:
    """
    Audits the availability and naming conventions of Tenable.io scanners.

    Attributes:
        tio (TenableIO): An instance of the authenticated Tenable.io API client.
    """

    def __init__(self, tio_client):
        """
        Initializes the module with the Tenable.io client.

        Args:
            tio_client (TenableIO): The API client used to query scanner data.
        """
        self.tio = tio_client

    def run_assessment(self):
        """
        Analyzes the health of all scanners and identifies offline infrastructure.

        Iterates through the scanner list, cleans technical UUID names for 
        readability, and flags non-operational sensors.

        Returns:
            dict: Contains summary statistics (total/offline) and the detailed 
                  list of offline scanners for the report appendix.
        """
        scanners = self.tio.scanners.list()
        offline_list = []
        total_count = 0
        offline_count = 0

        # Regular expression to identify system-generated UUIDs (technical names)
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

        for scanner in scanners:
            total_count += 1
            status = str(scanner.get('status', 'off')).lower()
            raw_name = scanner.get('name', 'Unknown')
            scanner_type = scanner.get('type', 'N/A')
            
            # If the name is a UUID, replace it with a legible asset label
            if re.search(uuid_pattern, raw_name):
                friendly_name = f"ID-ASSET ({scanner_type.upper()})"
            else:
                friendly_name = raw_name

            # Flag scanners that are not 'on' or 'on-line'
            if status not in ['on-line', 'on']:
                offline_count += 1
                offline_list.append(
                    f"RESOURCE: {friendly_name:<35} | TYPE: {scanner_type:<12} | STATUS: {status.upper()}"
                )

        return {
            "stats": {
                "total": total_count, 
                "offline": offline_count
            },
            "offline_list": sorted(offline_list)
        }