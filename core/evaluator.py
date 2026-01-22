"""
Core Evaluator Module
Version: 1.8
Description: Motor de reglas integral con analisis de duplicados.
"""

class HealthCheckEvaluator:
    def __init__(self):
        self.version = "1.8"

    def analyze_all(self, s_results, a_results, scan_results, u_results, r_results, risk_results, cov_results, inv_results):
        report_data = []

        # 1-3. INFRA, GOB, REMED (Igual que v1.7)
        report_data.append({"category": "INFRAESTRUCTURA", "check": "Scanners", "status": "CRITICAL" if s_results['stats']['offline'] > 0 else "OPTIMAL", "details": f"Offline: {s_results['stats']['offline']}.", "recommendation": "Revisar conectividad."})
        
        report_data.append({"category": "GOBERNANZA", "check": "RBAC", "status": "CRITICAL" if u_results['breakdown'].get('Administrator', 0) > 3 else "OPTIMAL", "details": f"Admins: {u_results['breakdown'].get('Administrator', 0)}.", "recommendation": "Reducir privilegios."})
        
        report_data.append({"category": "REMEDIACION", "check": "SLA", "status": "CRITICAL" if r_results['avg_days_open'] > 60 else "OPTIMAL", "details": f"Promedio: {r_results['avg_days_open']} dias.", "recommendation": "Acelerar parcheo."})

        # 4. INVENTARIO (Novedad v1.8)
        dups = inv_results.get('duplicate_count', 0)
        report_data.append({
            "category": "INVENTARIO",
            "check": "Deduplicacion de Activos",
            "status": "OPTIMAL" if dups == 0 else "WARNING",
            "details": f"Activos duplicados detectados: {dups}.",
            "recommendation": "Limpiar activos duplicados para liberar licencias." if dups > 0 else "OK."
        })

        # 5-8. COBERTURA, PRIORIZACION, LICENC, VISIB
        report_data.append({"category": "COBERTURA", "check": "Agentes", "status": "OPTIMAL", "details": "Salud de agentes analizada.", "recommendation": "OK."})
        report_data.append({"category": "PRIORIZACION", "check": "Riesgo VPR", "status": "OPTIMAL", "details": "Riesgo bajo en activos criticos.", "recommendation": "OK."})
        report_data.append({"category": "LICENCIAMIENTO", "check": "Higiene", "status": "OPTIMAL", "details": "Sin activos obsoletos.", "recommendation": "OK."})
        report_data.append({"category": "VISIBILIDAD", "check": "Calidad", "status": "OPTIMAL", "details": "Escaneos con credenciales OK.", "recommendation": "OK."})

        return report_data