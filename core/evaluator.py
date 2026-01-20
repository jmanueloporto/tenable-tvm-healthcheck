class HealthCheckEvaluator:
    def __init__(self):
        self.STALE_THRESHOLD = 90

    def analyze_all(self, s_results, a_results, scan_results, u_results):
        report_data = []

        # --- INFRAESTRUCTURA ---
        s_stats = s_results.get('stats', {})
        offline = s_stats.get('offline', 0)
        report_data.append({
            "category": "INFRAESTRUCTURA",
            "check": "Disponibilidad de Scanners",
            "status": "OPTIMAL" if offline == 0 else "CRITICAL",
            "details": f"Total: {s_stats.get('total', 0)}, Offline: {offline}.",
            "recommendation": "Restablecer conectividad de sensores." if offline > 0 else "OK."
        })

        # --- GOBERNANZA: RBAC ---
        gov_stats = u_results.get('breakdown', {})
        total_u = u_results.get('total_users', 0)
        admins = gov_stats.get('Administrator', 0)
        
        # Alerta si mas del 10% de los usuarios son administradores
        rbac_status = "CRITICAL" if admins > 3 else "OPTIMAL"
        
        breakdown_str = ", ".join([f"{k}: {v}" for k, v in gov_stats.items()])
        
        report_data.append({
            "category": "GOBERNANZA",
            "check": "Distribucion de Roles (RBAC)",
            "status": rbac_status,
            "details": f"Total: {total_u}. Desglose: {breakdown_str}",
            "recommendation": f"Se detectaron {admins} Administradores. Reducir privilegios para cumplir con el principio de menor privilegio." if rbac_status == "CRITICAL" else "Distribucion adecuada."
        })

        # --- LICENCIAMIENTO ---
        stale = a_results.get('stats', {}).get('stale_assets', 0)
        report_data.append({
            "category": "LICENCIAMIENTO",
            "check": "Higiene de Activos",
            "status": "OPTIMAL" if stale == 0 else "WARNING",
            "details": f"Stale assets: {stale}.",
            "recommendation": "Configurar purga automatica." if stale > 0 else "OK."
        })

        # --- VISIBILIDAD ---
        sc_stats = scan_results.get('stats', {})
        failures = sc_stats.get('auth_failures', 0)
        report_data.append({
            "category": "VISIBILIDAD",
            "check": "Calidad de Escaneo",
            "status": "OPTIMAL" if failures == 0 else "WARNING",
            "details": f"Errores de visibilidad: {failures}.",
            "recommendation": "Validar credenciales de escaneo." if failures > 0 else "OK."
        })

        return report_data