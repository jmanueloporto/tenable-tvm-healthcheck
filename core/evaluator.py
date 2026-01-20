class HealthCheckEvaluator:
    """
    Motor de logica para transformar hallazgos tecnicos en 
    recomendaciones estrategicas de consultoria.
    """
    
    def __init__(self):
        self.STALE_THRESHOLD = 90

    def analyze_infrastructure(self, scanner_data):
        recommendations = []
        stats = scanner_data.get('stats', {})

        if stats.get('offline', 0) > 0:
            recommendations.append({
                "severity": "CRITICAL",
                "finding": f"Existen {stats['offline']} scanners fuera de linea.",
                "recommendation": "Restablecer la conectividad de los sensores para garantizar la cobertura de escaneo."
            })

        if stats.get('outdated', 0) > 0:
            recommendations.append({
                "severity": "MEDIUM",
                "finding": f"{stats['outdated']} scanners requieren actualizacion.",
                "recommendation": "Actualizar el software de Nessus para acceder a las ultimas firmas de vulnerabilidades."
            })
            
        return recommendations

    def analyze_licensing(self, asset_data):
        recommendations = []
        stale_count = asset_data.get('stats', {}).get('stale_assets', 0)

        if stale_count > 0:
            recommendations.append({
                "severity": "LOW",
                "finding": f"Se detectaron {stale_count} activos inactivos (>90 dias).",
                "recommendation": "Implementar reglas de purga automatica para optimizar el uso de licencias."
            })
            
        return recommendations

    def analyze_scans(self, scan_data):
        """Analiza la visibilidad y salud de los escaneos."""
        recommendations = []
        stats = scan_data.get('stats', {})

        if stats.get('auth_failures', 0) > 0:
            recommendations.append({
                "severity": "HIGH",
                "finding": f"Se detectaron {stats['auth_failures']} escaneos con baja visibilidad o errores.",
                "recommendation": "Validar las credenciales de escaneo y permisos de red para asegurar un analisis profundo (deep scan)."
            })
            
        return recommendations