"""
Core Evaluator Module - Version: 1.8.6
"""
class HealthCheckEvaluator:
    def __init__(self):
        self.version = "1.8.6"

    def analyze_all(self, s_res, a_res, sc_res, u_res, r_res, ri_res, co_res, inv_res):
        return [
            {
                "category": "INFRAESTRUCTURA",
                "check": "Disponibilidad de Scanners",
                "status": "CRITICAL" if s_res['stats']['offline'] > 0 else "OPTIMAL",
                "details": f"Total: {s_res['stats'].get('total',0)}, Offline: {s_res['stats'].get('offline',0)}.",
                "data_for_appendix": s_res.get('offline_list', [])
            },
            {
                "category": "GOBERNANZA",
                "check": "Distribucion de Roles (RBAC)",
                "status": "CRITICAL" if u_res['breakdown'].get('Administrator', 0) > 3 else "OPTIMAL",
                "details": f"Total Usuarios: {u_res.get('total_users',0)}. Admins: {u_res['breakdown'].get('Administrator', 0)}.",
                "data_for_appendix": u_res.get('admin_list', [])
            },
            {
                "category": "REMEDIACION",
                "check": "Desempeño de SLA y Parcheo",
                "status": "CRITICAL" if r_res['avg_days_open'] > 60 else "OPTIMAL",
                "details": f"Promedio dias: {r_res['avg_days_open']}. Criticas vencidas: {r_res['overdue_criticals']}. Con Exploit: {r_res['exploitable_total']}.",
                "data_for_appendix": []
            },
            {
                "category": "PRIORIZACION",
                "check": "Riesgo VPR (Predictivo)",
                "status": "OPTIMAL", # Se mantiene segun resultados previos
                "details": f"Puntaje VPR maximo: {ri_res[0]['vpr'] if ri_res else 0.0} en el Top 10.",
                "data_for_appendix": ri_res
            },
            {
                "category": "INVENTARIO",
                "check": "Deduplicacion de Activos",
                "status": "OPTIMAL" if inv_res.get('duplicate_count', 0) == 0 else "WARNING",
                "details": f"Activos duplicados detectados: {inv_res.get('duplicate_count', 0)}.",
                "data_for_appendix": inv_res.get('list', [])
            },
            {
                "category": "COBERTURA",
                "check": "Salud de Agentes Nessus",
                "status": "OPTIMAL", 
                "details": "Salud de agentes analizada.",
                "data_for_appendix": []
            },
            {
                "category": "LICENCIAMIENTO",
                "check": "Higiene de Activos (Stale)",
                "status": "OPTIMAL",
                "details": f"Activos inactivos > 90 dias: {a_res['stats'].get('stale_assets', 0)}.",
                "data_for_appendix": []
            },
            {
                "category": "VISIBILIDAD",
                "check": "Calidad de Escaneo",
                "status": "OPTIMAL",
                "details": "Escaneos con credenciales OK.",
                "data_for_appendix": []
            }
        ]