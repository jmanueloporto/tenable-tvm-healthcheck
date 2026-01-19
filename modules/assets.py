from datetime import datetime, timezone

class AssetHealthModule:
    """
    Evalúa la higiene del inventario de activos y el impacto en licenciamiento.
    Alineado con la revisión de almacenamiento y configuración.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def run_hygiene_check(self, stale_days=90):
        """
        Identifica activos 'stale' (no vistos recientemente).
        """
        assets = self.tio.assets.list()
        now = datetime.now(timezone.utc)
        
        findings = {
            "stats": {"total_assets": 0, "stale_assets": 0},
            "stale_list": []
        }

        for asset in assets:
            findings["stats"]["total_assets"] += 1
            
            # Obtener la última vez que se vio el activo
            last_seen_str = asset.get('updated_at')
            if last_seen_str:
                # pyTenable suele devolver objetos datetime o strings ISO
                # Calculamos la antigüedad
                last_seen = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                delta = (now - last_seen).days
                
                if delta > stale_days:
                    findings["stats"]["stale_assets"] += 1
                    findings["stale_list"].append({
                        "id": asset.get('id'),
                        "name": asset.get('name') or asset.get('ipv4', ['N/A'])[0],
                        "days_inactive": delta
                    })

        return findings