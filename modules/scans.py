class ScanHealthModule:
    """
    Evalúa la configuración y efectividad de los escaneos.
    Alineado con la revisión de políticas y mejores prácticas.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def audit_performance(self):
        """
        Analiza los escaneos recientes para detectar brechas de visibilidad.
        """
        # Obtenemos la lista de escaneos realizados
        scans = self.tio.scans.list()
        findings = {
            "stats": {"total_scans": 0, "completed": 0, "failed": 0},
            "visibility_gaps": []
        }

        for scan in scans:
            findings["stats"]["total_scans"] += 1
            status = scan.get('status')
            
            if status == 'completed':
                findings["stats"]["completed"] += 1
                # En un Health Check real, aquí verificaríamos el 'auth_success' 
                # detallado de cada scan_id para reportar falta de credenciales[cite: 49].
            elif status in ['error', 'canceled', 'aborted']:
                findings["stats"]["failed"] += 1
                findings["visibility_gaps"].append({
                    "name": scan.get('name'),
                    "issue": f"Escaneo con estado: {status}"
                })

        return findings