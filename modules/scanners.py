"""
Scanner Health Module - Version: 1.8.7
"""
class ScannerHealthModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def run_assessment(self):
        scanners = self.tio.scanners.list()
        offline_list = []
        total = 0
        offline_count = 0

        for s in scanners:
            total += 1
            status = str(s.get('status', 'off')).lower()
            name = s.get('name', 'Unknown Scanner')
            
            if status not in ['on-line', 'on']:
                offline_count += 1
                offline_list.append(f"NOMBRE: {name:<35} | ESTADO: {status.upper()}")

        return {
            "stats": {"total": total, "offline": offline_count},
            "offline_list": sorted(offline_list)
        }