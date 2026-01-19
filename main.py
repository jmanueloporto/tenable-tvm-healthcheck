from core.connection import TenableConnection
from modules.scanners import ScannerHealthModule
from modules.assets import AssetHealthModule
from core.evaluator import HealthCheckEvaluator
from reports.generator import ReportGenerator

def main():
    try:
        # 1. Conexión
        tio = TenableConnection().get_client()
        
        # 2. Diagnóstico
        s_data = ScannerHealthModule(tio).run_assessment()
        a_data = AssetHealthModule(tio).run_hygiene_check()

        # 3. Evaluación (Lógica de Consultor)
        engine = HealthCheckEvaluator()
        infra_finding = engine.evaluate_infrastructure(s_data['stats'])
        asset_finding = engine.evaluate_assets(a_data['stats'])

        # 4. Generación de Reporte Físico
        reporter = ReportGenerator()
        file_path = reporter.generate_executive_summary(
            s_data, a_data, infra_finding, asset_finding
        )

        print(f"\n[OK] Health Check completado.")
        print(f"[INFO] El Resumen Ejecutivo ha sido generado en: {file_path}")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()