"""
Risk & VPR Priority Module
Version: 1.6.1
Description: Identifica los activos con mayor puntaje VPR corrigiendo el metodo de ordenamiento.
"""

class RiskModule:
    def __init__(self, tio_client):
        self.version = "1.6.1"
        self.tio = tio_client

    def get_top_risk_assets(self):
        """
        Obtiene los activos y los ordena por VPR (Vulnerability Priority Rating).
        """
        top_assets = []
        try:
            # Obtenemos la lista de activos (limitamos a 100 para procesar rapido)
            assets = self.tio.assets.list()
            
            # Extraemos la data necesaria
            processed_assets = []
            for asset in assets:
                processed_assets.append({
                    "name": asset.get('hostname') or (asset.get('ipv4') or ["Unknown"])[0],
                    "vpr": float(asset.get('vpr_score') or 0.0),
                    "id": asset.get('id')
                })
            
            # Ordenamos por VPR de mayor a menor
            sorted_assets = sorted(processed_assets, key=lambda x: x['vpr'], reverse=True)
            
            # Retornamos solo los top 10
            return sorted_assets[:10]
        except Exception as e:
            print(f"Error en RiskModule: {e}")
            return []