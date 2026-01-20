class HealthCheckEvaluator:
    """
    Motor de evaluacion integral que clasifica hallazgos por estado
    e incluye recomendaciones de Gobernanza (RBAC/SLA).
    """
    def __init__(self):
        self.STALE_THRESHOLD = 90

    def analyze_all(self, s_results, a_results, scan_results):
        report_data = []

        # --- CATEGORIA: INFRAESTRUCTURA ---
        s_stats = s_results.get('stats', {})
        offline = s_stats.get('offline', 0)
        infra_status = "OPTIMAL" if offline == 0 else "CRITICAL"
        
        report_data.append({
            "category": "INFRAESTRUCTURA",
            "check": "Disponibilidad de Scanners",
            "status": infra_status,
            "details": f"Total: {s_stats.get('total', 0)}, Online: {s_stats.get('total', 0) - offline}, Offline: {offline}.",
            "recommendation": "Sin accion requerida." if infra_status == "OPTIMAL" else "Urgente: Restablecer conectividad de red o servicios de Nessus en sensores afectados."
        })

        # --- CATEGORIA: LICENCIAMIENTO ---
        stale = a_results.get('stats', {}).get('stale_assets', 0)
        lic_status = "OPTIMAL" if stale == 0 else "WARNING"
        
        report_data.append({
            "category": "LICENCIAMIENTO",
            "check": "Higiene de Activos (Stale Assets)",
            "status": lic_status,
            "details": f"Activos totales: {a_results.get('stats', {}).get('total_assets')}. Activos inactivos detectados: {stale}.",
            "recommendation": "Higiene de activos adecuada." if lic_status == "OPTIMAL" else f"Optimizar licenciamiento eliminando activos no vistos en {self.STALE_THRESHOLD} dias mediante reglas de purga."
        })

        # --- CATEGORIA: VISIBILIDAD ---
        sc_stats = scan_results.get('stats', {})
        failures = sc_stats.get('auth_failures', 0)
        scan_status = "OPTIMAL" if failures == 0 else "WARNING"
        
        report_data.append({
            "category": "VISIBILIDAD",
            "check": "Calidad de Escaneo y Credenciales",
            "status": scan_status,
            "details": f"Escaneos completados: {sc_stats.get('authenticated', 0)}. Escaneos con errores/baja visibilidad: {failures}.",
            "recommendation": "Configuracion de escaneo eficiente." if scan_status == "OPTIMAL" else "Revisar logs de escaneo para identificar fallos de autenticacion y asegurar visibilidad profunda."
        })

        # --- CATEGORIA: GOBERNANZA (RECOMENDACIONES CONSULTIVAS) ---
        report_data.append({
            "category": "GOBERNANZA",
            "check": "Revision de Roles (RBAC)",
            "status": "MANUAL_REVIEW",
            "details": "Evaluacion de privilegios y segregacion de funciones.",
            "recommendation": "Aplicar el principio de menor privilegio. Validar que los perfiles de 'Basic' no tengan acceso a configuraciones globales o gestion de scanners."
        })

        report_data.append({
            "category": "GOBERNANZA",
            "check": "Analisis de SLA de Remediacion",
            "status": "MANUAL_REVIEW",
            "details": "Revision de tiempos de respuesta ante vulnerabilidades.",
            "recommendation": "Establecer metricas de remediacion: Criticas (7 dias), Altas (30 dias). Configurar SLAs en Tenable para monitorear el cumplimiento por parte de los dueños de activos."
        })

        return report_data