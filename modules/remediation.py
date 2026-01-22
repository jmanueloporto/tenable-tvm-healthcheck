"""
Remediation & SLA Module
Version: 1.5
Description: Calculo de tiempos de respuesta y detección de exploits.
"""
from datetime import datetime, timezone

class RemediationModule:
    def __init__(self, tio_client):
        self.version = "1.5"
        self.tio = tio_client

    def calculate_sla_performance(self):
        stats = {"avg_days_open": 0, "overdue_criticals": 0, "overdue_highs": 0, "exploitable_total": 0, "total_analyzed": 0}
        try:
            vulns = self.tio.exports.vulns(severity=['critical', 'high'], state=['open'])
            count = 0
            total_days = 0
            now = datetime.now(timezone.utc)

            for v in vulns:
                count += 1
                first_found = v.get('first_found')
                severity = v.get('severity')
                has_exploit = v.get('has_exploit', False)
                
                if first_found:
                    found_date = datetime.fromisoformat(first_found.replace('Z', '+00:00'))
                    days_open = (now - found_date).days
                    total_days += days_open
                    if severity == 'critical' and days_open > 14: stats["overdue_criticals"] += 1
                    elif severity == 'high' and days_open > 30: stats["overdue_highs"] += 1
                
                if has_exploit: stats["exploitable_total"] += 1
                if count >= 1000: break 

            if count > 0:
                stats["avg_days_open"] = round(total_days / count)
                stats["total_analyzed"] = count
            return stats
        except Exception as e:
            return {"error": str(e), "avg_days_open": 0, "overdue_criticals": 0}