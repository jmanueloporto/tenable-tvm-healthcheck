"""
Inventory & Deduplication Module
Version: 1.8
Description: Identifica activos duplicados para optimizar el consumo de licencias.
"""

class InventoryModule:
    def __init__(self, tio_client):
        self.version = "1.8"
        self.tio = tio_client

    def find_duplicates(self):
        """
        Busca posibles duplicados basados en el hostname.
        """
        duplicates = []
        seen_hosts = {}
        try:
            assets = self.tio.assets.list()
            for asset in assets:
                hostname = asset.get('hostname')
                if hostname:
                    hostname = hostname[0].lower() if isinstance(hostname, list) else hostname.lower()
                    if hostname in seen_hosts:
                        duplicates.append(hostname)
                    else:
                        seen_hosts[hostname] = asset.get('id')
            
            return {"duplicate_count": len(duplicates), "list": duplicates}
        except Exception as e:
            print(f"Error en InventoryModule: {e}")
            return {"duplicate_count": 0, "list": []}