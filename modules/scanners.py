"""
Scanner Health Module - Version: 1.8.8
"""
import re

class ScannerHealthModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def run_assessment(self):
        scanners = self.tio.scanners.list()
        offline_list = []
        total = 0
        offline_count = 0
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

        for s in scanners:
            total += 1
            status = str(s.get('status', 'off')).lower()
            raw_name = s.get('name', 'Unknown')
            scanner_type = s.get('type', 'N/A')
            
            name = f"ID-ASSET ({scanner_type.upper()})" if re.search(uuid_pattern, raw_name) else raw_name

            if status not in ['on-line', 'on']:
                offline_count += 1
                offline_list.append(f"RECURSO: {name:<35} | TIPO: {scanner_type:<12} | ESTADO: {status.upper()}")

        return {
            "stats": {"total": total, "offline": offline_count},
            "offline_list": sorted(offline_list)
        }