class HealthCheckEvaluator:
    """
    Motor de logica para transformar hallazgos tecnicos en 
    recomendaciones estrategicas de consultoria.
    """
    
    def __init__(self):
        # Definimos los umbrales de mejores practicas segun Tenable
        self.STALE_THRESHOLD = 90  # dias para considerar un activo inactivo

    def analyze_infrastructure(self, scanner_data):
        """Genera recomendaciones basadas en el estado de los scanners."""
        recommendations = []
        stats = scanner_data.get('stats', {})

        if stats.get('offline', 0) > 0:
            recommendations.append({
                "severity": "CRITICAL",
                "finding": f"Existen {stats['offline']} scanners fuera de linea.",
                "recommendation": "Restablecer la conectividad de los sensores para garantizar la cobertura de escaneo y evitar puntos ciegos."
            })

        if stats.get('outdated', 0) > 0:
            recommendations.append({
                "severity": "MEDIUM",
                "finding": f"{stats['outdated']} scanners requieren actualizacion.",
                "recommendation": "Actualizar el software de Nessus para acceder a las ultimas capacidades de deteccion y correcciones."
            })
            
        return recommendations

    def analyze_licensing(self, asset_data):
        """Genera recomendaciones basadas en la higiene de activos."""
        recommendations = []
        stale_count = asset_data.get('stats', {}).get('stale_assets', 0)

        if stale_count > 0:
            recommendations.append({
                "severity": "LOW",
                "finding": f"Se detectaron {stale_count} activos inactivos por mas de {self.STALE_THRESHOLD} dias.",
                "recommendation": "Implementar reglas de purga automatica para liberar licencias y mejorar el rendimiento."
            })
            
        return recommendations