import sys
from core.connection import TenableConnection
from core.evaluator import HealthCheckEvaluator
from modules.scanners import ScannerHealthModule
from modules.assets import AssetHealthModule
from modules.scans import ScanHealthModule
from reports.generator import ReportGenerator

def run_complete_health_check():
    print("\n" + "="*50)
    print("      TENABLE AUTOMATED HEALTH CHECK TOOL")
    print("="*50)
    
    try:
        # 1. Conexion
        print("[*] Estableciendo conexion con Tenable VM...")
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        # 2. Diagnosticos
        print("[*] Analizando infraestructura de scanners...")
        s_results = ScannerHealthModule(tio).run_assessment()

        print("[*] Analizando inventario de activos...")
        a_results = AssetHealthModule(tio).run_hygiene_check(stale_days=90)

        print("[*] Analizando calidad y visibilidad de escaneos...")
        scan_results = ScanHealthModule(tio).audit_credentials_health()

        # 3. Evaluacion Estrategica
        print("[*] Procesando hallazgos y recomendaciones...")
        evaluator = HealthCheckEvaluator()
        
        infra_advices = evaluator.analyze_infrastructure(s_results)
        license_advices = evaluator.analyze_licensing(a_results)
        scan_advices = evaluator.analyze_scans(scan_results)

        all_advices = infra_advices + license_advices + scan_advices

        # 4. Generacion de Reportes
        print("[*] Generando entregables finales...")
        full_data = {
            "infrastructure": s_results,
            "inventory": a_results,
            "scans": scan_results,
            "recommendations": all_advices
        }
        
        reporter = ReportGenerator()
        reporter.save_json_report(full_data)
        reporter.save_txt_summary(all_advices)

        # 5. Salida por Consola
        print("\n" + "!"*10 + " RECOMENDACIONES DE CONSULTORIA " + "!"*10)
        
        if not all_advices:
            print("[+] Salud de la plataforma optima.")
        else:
            for advice in all_advices:
                print(f"[{advice['severity']}] {advice['finding']}")
                print(f" -> SUGERENCIA: {advice['recommendation']}\n")

        print("="*50)
        print("PROCESO FINALIZADO EXITOSAMENTE")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR CRITICO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_complete_health_check()