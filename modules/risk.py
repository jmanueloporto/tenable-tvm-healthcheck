"""
Risk Intelligence Module
Version: 2.1.2 (Stable)
"""
class RiskModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def get_top_risk_assets(self):
        top_vulns = []
        try:
            # Formato corregido de la v1.9.1: un solo string de rango
            vulns = self.tio.exports.vulns(vpr_score=['0.1:10.0'], state=['open'])
            for v in vulns:
                top_vulns.append({
                    "plugin_name": v.get('plugin_name') or "Unknown",
                    "vpr": v.get('vpr_score', 0.0),
                    "asset": v.get('asset', {}).get('hostname') or "N/A"
                })
                if len(top_vulns) >= 10: break
            return sorted(top_vulns, key=lambda x: x['vpr'], reverse=True)
        except:
            return []
