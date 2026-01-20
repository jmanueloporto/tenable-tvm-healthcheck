class ScanHealthModule:
    """
    Evalua la calidad de los escaneos enfocandose en la visibilidad 
    y el uso de credenciales.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def audit_credentials_health(self):
        """
        Analiza los escaneos recientes para identificar fallos de autenticacion.
        """
        scans = self.tio.scans.list()
        findings = {
            "stats": {"total_scans": 0, "authenticated": 0, "auth_failures": 0},
            "low_visibility_scans": []
        }

        # Analizamos los ultimos 20 escaneos para tener una muestra representativa
        for scan in scans[:20]:
            findings["stats"]["total_scans"] += 1
            status = scan.get('status')

            if status == 'completed':
                # En un Health Check profundo se validaria el plugin 21745
                findings["stats"]["authenticated"] += 1
            elif status in ['error', 'aborted', 'canceled']:
                findings["stats"]["auth_failures"] += 1
                findings["low_visibility_scans"].append({
                    "name": scan.get('name'),
                    "status": status
                })

        return findings