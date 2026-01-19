class ScannerHealthModule:
    """
    Analiza la resiliencia y efectividad de los sensores de red[cite: 23].
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def run_assessment(self):
        """Identifica scanners offline o desactualizados."""
        scanners = self.tio.scanners.list()
        findings = {
            "critical_issues": [],
            "stats": {"total": 0, "offline": 0, "outdated": 0}
        }

        for s in scanners:
            findings["stats"]["total"] += 1
            name = s.get('name', 'Desconocido')
            
            # Verificar estado (Resiliencia) [cite: 32]
            if s.get('status') != 'on':
                findings["stats"]["offline"] += 1
                findings["critical_issues"].append(f"Scanner '{name}' está OFFLINE.")
            
            # Verificar actualización (Configuración) 
            if s.get('outdated'):
                findings["stats"]["outdated"] += 1
                findings["critical_issues"].append(f"Scanner '{name}' requiere actualización de software/plugins.")

        return findings