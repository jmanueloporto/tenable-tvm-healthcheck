"""
Risk Intelligence Module
Version: 2.0.0
Description: Extracts high-impact vulnerabilities using Tenable's VPR scoring.
"""
class RiskModule:
    """
    Interfaces with Tenable VPR to identify the most dangerous open threats.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def get_top_risk_assets(self):
        """
        Exports vulnerabilities with high VPR scores.
        
        Returns:
            list: Top 10 critical risks with associated assets.
        """
        top_vulns = []
        try:
            # Filtering for dynamic scores above 0.1 to find relevant data
            vulns = self.tio.exports.vulns(vpr_score=['0.1', '10.0'], state=['open'])
            
            for v in vulns:
                top_vulns.append({
                    "plugin_name": v.get('plugin', {}).get('name') or v.get('plugin_name', 'Unknown'),
                    "vpr": v.get('vpr_score', 0.0),
                    "asset": v.get('asset', {}).get('hostname') or "N/A"
                })
                if len(top_vulns) >= 10: break
            
            return sorted(top_vulns, key=lambda x: x['vpr'], reverse=True)
        except Exception:
            return []