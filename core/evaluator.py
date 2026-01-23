"""
Core Evaluator Module - Version: 1.9.0
"""
class HealthCheckEvaluator:
    def __init__(self):
        self.version = "1.9.0"

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
                "status": "CRITICAL" if u_res['breakdown'].get('Administrator', 0) > 5 else "OPTIMAL",
                "details": f"Total Usuarios: {u_res.get('total_users',0)}. Admins: {u_res['breakdown'].get('Administrator', 0)}.",
                "data_for_appendix": u_res.get('admin_list', [])
            },
            {
                "category": "PRIORIZACION",
                "check": "Riesgo Predictivo (VPR Intelligence)",
                "status": "CRITICAL" if any(x.get('vpr', 0) > 8.0 for x in ri_res) else "OPTIMAL",
                "details": f"Hallazgos VPR criticos analizados: {len(ri_res)}.",
                "data_for_appendix": ri_res
            },
            {
                "category": "INVENTARIO",
                "check": "Higiene y Licenciamiento",
                "status": "OPTIMAL" if inv_res.get('duplicate_count', 0) == 0 else "WARNING",
                "details": f"Duplicados: {inv_res.get('duplicate_count', 0)}. Stale (>90d): {a_res['stats'].get('stale_assets', 0)}.",
                "data_for_appendix": inv_res.get('list', [])
            },
            {
                "category": "REMEDIACION",
                "check": "SLA y Deuda Tecnica",
                "status": "CRITICAL" if r_res['avg_days_open'] > 60 else "OPTIMAL",
                "details": f"Promedio: {r_res['avg_days_open']} dias. Criticas vencidas: {r_res['overdue_criticals']}.",
                "data_for_appendix": r_res.get('oldest_vulns', [])
            }
        ]