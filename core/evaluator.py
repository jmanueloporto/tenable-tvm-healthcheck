class HealthCheckEvaluator:
    """
    Motor que compara datos técnicos contra las recomendaciones 
    de Tenable detalladas en el Services Brief.
    """
    def __init__(self):
        # Umbrales basados en mejores prácticas de consultoría
        self.thresholds = {
            "max_offline_scanners_pct": 10,
            "max_stale_assets_pct": 15
        }

    def evaluate_infrastructure(self, scanner_stats):
        """Evalúa si la infraestructura es resiliente[cite: 23]."""
        total = scanner_stats['total']
        offline = scanner_stats['offline']
        
        if total == 0:
            return "Crítico: No se detectaron scanners en el entorno."

        offline_pct = (offline / total) * 100
        if offline_pct > self.thresholds["max_offline_scanners_pct"]:
            return f"Alerta: {offline_pct:.1f}% de scanners offline. Riesgo de resiliencia[cite: 23]."
        
        return "Infraestructura saludable y resiliente."

    def evaluate_assets(self, asset_stats):
        """Evalúa la higiene y optimización del almacenamiento."""
        total = asset_stats['total_assets']
        stale = asset_stats['stale_assets']
        
        if total == 0: return "Sin activos detectados."

        stale_pct = (stale / total) * 100
        if stale_pct > self.thresholds["max_stale_assets_pct"]:
            return f"Recomendación: {stale_pct:.1f}% de activos stale. Realizar purga para optimizar licenciamiento."
        
        return "Higiene de activos dentro de parámetros óptimos."