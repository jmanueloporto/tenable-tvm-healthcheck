"""
Core Evaluator Module
Version: 1.7
Description: Motor de reglas incluyendo analisis de cobertura de agentes.
"""

class HealthCheckEvaluator:
    def __init__(self):
        self.version = "1.7"
        self.STALE_THRESHOLD = 90

    def analyze_all(self, s_results, a_results, scan_results, u_results, r_results, risk_results, cov_results):
        report_data = []

        # 1. INFRAESTRUCTURA (Scanners)
        s_stats = s_results.get('stats', {})
        report_data.append({
            "category": "INFRAESTRUCTURA",
            "check": "Disponibilidad de Scanners",
            "status": "OPTIMAL" if s_stats.get('offline', 0) == 0 else "CRITICAL",
            "details": f"Total: {s_stats.get('total', 0)}, Offline: {s_stats.get('offline', 0)}.",
            "recommendation": "Restablecer conectividad de sensores."
        })

        # 2. GOBERNANZA
        gov_stats = u_results.get('breakdown', {})
        admins = gov_stats.get('Administrator', 0)
        report_data.append({
            "category": "GOBERNANZA",
            "check": "Distribucion de Roles (RBAC)",
            "status": "CRITICAL" if admins > 3 else "OPTIMAL",
            "details": f"Total Usuarios: {u_results.get('total_users')}. Admins: {admins}.",
            "recommendation": "Reducir administradores (Principio de Menor Privilegio)."
        })

        # 3. REMEDIACION
        avg_days = r_results.get('avg_days_open', 0)
        overdue_c = r_results.get('overdue_criticals', 0)
        exploits = r_results.get('exploitable_total', 0)
        status_rem = "OPTIMAL"
        if avg_days > 30 or overdue_c > 0 or exploits > 0: status_rem = "WARNING"
        if avg_days > 60 or overdue_c > 10 or exploits > 5: status_rem = "CRITICAL"
        report_data.append({"category": "REMEDIACION", "check": "Eficacia de Parcheo", "status": status_rem, "details": f"Promedio dias: {avg_days}. Vencidas: {overdue_c}.", "recommendation": "Priorizar remediacion."})

        # 4. COBERTURA (Novedad v1.7)
        total_ag = cov_results.get('total_agents', 0)
        off_ag = cov_results.get('offline', 0)
        status_cov = "OPTIMAL"
        if total_ag > 0 and (off_ag / total_ag) > 0.10: status_cov = "WARNING"
        if total_ag > 0 and (off_ag / total_ag) > 0.25: status_cov = "CRITICAL"
        
        report_data.append({
            "category": "COBERTURA",
            "check": "Salud de Agentes Nessus",
            "status": status_cov,
            "details": f"Total Agentes: {total_ag}. Offline: {off_ag}.",
            "recommendation": "Revisar servicios de agentes en estaciones de trabajo." if off_ag > 0 else "OK."
        })

        # 5. PRIORIZACION
        max_vpr = risk_results[0]['vpr'] if risk_results else 0
        status_risk = "OPTIMAL"
        if max_vpr >= 7.0: status_risk = "WARNING"
        if max_vpr >= 9.0: status_risk = "CRITICAL"
        report_data.append({"category": "PRIORIZACION", "check": "Riesgo VPR", "status": status_risk, "details": f"VPR Max: {max_vpr}.", "recommendation": "OK."})

        # 6. LICENCIAMIENTO & 7. VISIBILIDAD (Se mantienen igual)
        stale = a_results.get('stats', {}).get('stale_assets', 0)
        report_data.append({"category": "LICENCIAMIENTO", "check": "Higiene", "status": "OPTIMAL" if stale == 0 else "WARNING", "details": f"Stale: {stale}.", "recommendation": "Purga auto."})
        failures = scan_results.get('stats', {}).get('auth_failures', 0)
        report_data.append({"category": "VISIBILIDAD", "check": "Calidad", "status": "OPTIMAL" if failures == 0 else "WARNING", "details": f"Fallos: {failures}.", "recommendation": "Credenciales."})

        return report_data