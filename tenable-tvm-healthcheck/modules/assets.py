"""
Asset Hygiene Module
Version: 2.0.0
Description: Evaluates the health and status of assets in the Tenable workbench.
"""
from datetime import datetime, timedelta

class AssetHealthModule:
    """
    Analyzes asset data to identify stale or unlicensed records.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def run_hygiene_check(self):
        """
        Identifies 'stale' assets that haven't been seen in the last 90 days.
        
        Returns:
            dict: Statistics about asset hygiene.
        """
        assets = self.tio.assets.list()
        stale_threshold = datetime.now() - timedelta(days=90)
        stale_count = 0
        total_assets = 0

        for asset in assets:
            total_assets += 1
            last_seen_str = asset.get('last_seen')
            if last_seen_str:
                last_seen = datetime.strptime(last_seen_str.split('T')[0], '%Y-%m-%d')
                if last_seen < stale_threshold:
                    stale_count += 1

        return {
            "stats": {
                "total_assets": total_assets,
                "stale_assets": stale_count
            }
        }