"""
Remediation Performance Module
Version: 2.1.2 (Stable)
"""
from datetime import datetime
class RemediationModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def calculate_sla_performance(self):
        stats = {"avg_days_open": 0, "overdue_criticals": 0, "oldest_vulns": []}
        try:
            # Lista plana de severidades para evitar error de hashing
            vulns = self.tio.exports.vulns(severity=['critical', 'high'], state=['open'])
            all_vulns = []
            now = datetime.now()
            for v in vulns:
                first_found = v.get('first_found')
                if first_found:
                    dt = datetime.strptime(first_found.split('T')[0], '%Y-%m-%d')
                    days = (now - dt).days
                    all_vulns.append({"days_open": days, "severity": v.get('severity')})
                    if days > 30 and v.get('severity') == 'critical':
                        stats["overdue_criticals"] += 1
            if all_vulns:
                stats["avg_days_open"] = int(sum(v['days_open'] for v in all_vulns) / len(all_vulns))
            return stats
        except:
            return stats
