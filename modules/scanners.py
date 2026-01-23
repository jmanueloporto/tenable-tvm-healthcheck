"""
Scanner Health Module - Version: 1.8.6
"""
class ScannerHealthModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def run_assessment(self):
        scanners = self.tio.scanners.list()
        offline_list = []
        total = 0
        offline = 0

        for s in scanners:
            total += 1
            if s.get('status') != 'on-line':
                offline += 1
                offline_list.append(f"NOMBRE: {s.get('name'):<25} | IP: {s.get('ip', 'N/A'):<15} | ESTADO: {s.get('status')}")

        return {
            "stats": {"total": total, "offline": offline},
            "offline_list": sorted(offline_list)
        }