"""
Remediation Performance Module
Version: 2.0.0
Description: Measures time-to-remediate (SLA) and technical debt.
"""
from datetime import datetime

class RemediationModule:
    """
    Analyzes how long vulnerabilities stay open in the environment.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def calculate_sla_performance(self):
        """
        Calculates average days open and identifies the oldest critical vulnerabilities.
        """
        stats = {"avg_days_open": 0, "overdue_criticals": 0, "oldest_vulns": []}
        try:
            vulns = self.tio.exports.vulns(severity=['critical', 'high'], state=['open'])
            all_vulns = []
            now = datetime.now()

            for v in vulns:
                p_name = v.get('plugin_name') or v.get('plugin', {}).get('name') or "N/A"
                first_found = v.get('first_found')
                if first_found:
                    dt = datetime.strptime(first_found.split('T')[0], '%Y-%m-%d')
                    days = (now - dt).days
                    
                    vuln_data = {
                        "plugin_name": p_name,
                        "days_open": days,
                        "severity": v.get('severity')
                    }
                    all_vulns.append(vuln_data)
                    if days > 30 and v.get('severity') == 'critical':
                        stats["overdue_criticals"] += 1

            if all_vulns:
                stats["avg_days_open"] = int(sum(v['days_open'] for v in all_vulns) / len(all_vulns))
                stats["oldest_vulns"] = sorted(all_vulns, key=lambda x: x['days_open'], reverse=True)[:5]
            
            return stats
        except Exception:
            return stats