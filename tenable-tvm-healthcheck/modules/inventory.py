"""
Inventory De-duplication Module
Version: 2.0.0
Description: Detects duplicate asset records to optimize licensing.
"""
class InventoryModule:
    """
    Checks for multiple assets sharing the same hostname or IP address.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def find_duplicates(self):
        """
        Analyzes the asset workbench for duplicated hostnames.
        
        Returns:
            dict: Count and list of potential duplicate assets.
        """
        assets = self.tio.assets.list()
        seen_hosts = {}
        duplicates = []

        for asset in assets:
            hostname = asset.get('hostname')
            if hostname:
                if hostname in seen_hosts:
                    duplicates.append(f"DUPLICATE HOST: {hostname}")
                else:
                    seen_hosts[hostname] = asset.get('id')

        return {
            "duplicate_count": len(duplicates),
            "list": duplicates
        }