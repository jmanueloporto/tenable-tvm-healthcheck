"""
Core Evaluator Module
Version: 1.6
Description: Motor de reglas y calificacion de hallazgos incluyendo analisis de VPR.
"""

class HealthCheckEvaluator:
    def __init__(self):
        self.version = "1.6"
        self.STALE_THRESHOLD = 90

    def analyze_all(self, s_results, a_results, scan_results, u_results, r_results, risk_results):
        report_data = []

        # 1. INFRAESTRUCTURA
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
        
        report_data.append({
            "category": "REMEDIACION",
            "check": "Eficacia de Parcheo y Analisis de Exploit",
            "status": status_rem,
            "details": f"Promedio dias: {avg_days}. Criticas vencidas: {overdue_c}. Con Exploit: {exploits}.",
            "recommendation": "Priorizar vulnerabilidades con exploit activo."
        })

        # 4. PRIORIZACION (Novedad v1.6)
        max_vpr = max([a['vpr'] for a in risk_results]) if risk_results else 0
        status_risk = "OPTIMAL"
        if max_vpr >= 7.0: status_risk = "WARNING"
        if max_vpr >= 9.0: status_risk = "CRITICAL"

        report_data.append({
            "category": "PRIORIZACION",
            "check": "Activos de Alto Riesgo (VPR)",
            "status": status_risk,
            "details": f"Puntaje VPR maximo: {max_vpr} en el Top 10.",
            "recommendation": f"Enfocar recursos en el activo {risk_results[0]['name']} por alto riesgo de explotacion." if risk_results else "OK."
        })

        # 5. LICENCIAMIENTO
        stale = a_results.get('stats', {}).get('stale_assets', 0)
        report_data.append({
            "category": "LICENCIAMIENTO",
            "check": "Higiene de Activos (Stale)",
            "status": "OPTIMAL" if stale == 0 else "WARNING",
            "details": f"Activos inactivos > 90 dias: {stale}.",
            "recommendation": "Configurar reglas de purga automatica."
        })

        # 6. VISIBILIDAD
        failures = scan_results.get('stats', {}).get('auth_failures', 0)
        report_data.append({
            "category": "VISIBILIDAD",
            "check": "Calidad de Escaneo",
            "status": "OPTIMAL" if failures == 0 else "WARNING",
            "details": f"Fallos de autenticacion: {failures}.",
            "recommendation": "Validar credenciales de escaneo."
        })

        return report_data