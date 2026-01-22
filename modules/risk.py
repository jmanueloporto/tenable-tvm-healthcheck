"""
Risk & VPR Priority Module
Version: 1.6
Description: Identifica los activos con mayor puntaje VPR para remediación inmediata.
"""

class RiskModule:
    def __init__(self, tio_client):
        self.version = "1.6"
        self.tio = tio_client

    def get_top_risk_assets(self):
        """
        Obtiene los activos con mayor VPR (Vulnerability Priority Rating).
        """
        top_assets = []
        try:
            # Ordenamos por vpr_score descendente para traer los más peligrosos
            assets = self.tio.assets.list(sort=[('vpr_score', 'desc')], limit=10)
            
            for asset in assets:
                top_assets.append({
                    "name": asset.get('hostname') or asset.get('ipv4') or "Desconocido",
                    "vpr": asset.get('vpr_score', 0),
                    "id": asset.get('id')
                })
            
            return top_assets
        except Exception as e:
            print(f"Error en RiskModule: {e}")
            return []