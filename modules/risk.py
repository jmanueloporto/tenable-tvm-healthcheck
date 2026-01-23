"""
Risk Module - Version: 1.9.0
Description: Identifica las vulnerabilidades con mayor impacto dinámico (VPR) y sus activos.
"""
class RiskModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def get_top_risk_assets(self):
        # Buscamos las vulnerabilidades con mayor VPR (puntaje dinámico)
        # Filtramos por puntajes altos para obtener los riesgos reales
        top_vulns = []
        try:
            vulns = self.tio.exports.vulns(vpr_score=['0.1', '10.0'], state=['open'])
            
            for v in vulns:
                top_vulns.append({
                    "plugin_name": v.get('plugin', {}).get('name') or v.get('plugin_name', 'Unknown'),
                    "vpr": v.get('vpr_score', 0.0),
                    "asset": v.get('asset', {}).get('hostname') or "N/A"
                })
                # Limitamos a los 10 riesgos más altos detectados
                if len(top_vulns) >= 10: break
            
            # Si no hay nada con VPR, devolvemos una lista vacía para que el reporte lo maneje
            return sorted(top_vulns, key=lambda x: x['vpr'], reverse=True)
        except Exception:
            return []