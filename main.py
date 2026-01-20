import sys
from core.connection import TenableConnection
from core.evaluator import HealthCheckEvaluator
from modules.scanners import ScannerHealthModule
from modules.assets import AssetHealthModule
from reports.generator import ReportGenerator

def run_complete_health_check():
    print("\n" + "="*50)
    print("      TENABLE AUTOMATED HEALTH CHECK TOOL")
    print("="*50)
    
    try:
        # 1. Conexion (Core)
        print("[*] Estableciendo conexion con Tenable VM...")
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        # 2. Ejecucion de Diagnosticos (Modules)
        print("[*] Analizando infraestructura de scanners...")
        s_tool = ScannerHealthModule(tio)
        s_results = s_tool.run_assessment()

        print("[*] Analizando inventario de activos...")
        a_tool = AssetHealthModule(tio)
        a_results = a_tool.run_hygiene_check(stale_days=90)

        # 3. Evaluacion Estrategica (Evaluator)
        print("[*] Procesando hallazgos y recomendaciones...")
        evaluator = HealthCheckEvaluator()
        infra_advices = evaluator.analyze_infrastructure(s_results)
        license_advices = evaluator.analyze_licensing(a_results)
        
        all_advices = infra_advices + license_advices

        # 4. Generacion de Reportes (Reports)
        print("[*] Generando entregables en carpeta /reports...")
        full_data = {
            "infrastructure": s_results,
            "inventory": a_results,
            "recommendations": all_advices
        }
        
        reporter = ReportGenerator()
        # Ajuste: Guardamos el JSON detallado
        reporter.save_json_report(full_data)
        # Ajuste: Guardamos el TXT resumido para el consultor
        reporter.save_txt_summary(all_advices)

        # 5. Salida por Consola (Resumen Ejecutivo)
        print("\n" + "!"*10 + " RECOMENDACIONES DE CONSULTORIA " + "!"*10)
        
        if not all_advices:
            print("[+] No se detectaron brechas criticas. La salud es optima.")
        else:
            for advice in all_advices:
                print(f"[{advice['severity']}] {advice['finding']}")
                print(f" -> SUGERENCIA: {advice['recommendation']}\n")

        print("="*50)
        print("PROCESO FINALIZADO EXITOSAMENTE")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR CRITICO DURANTE LA EJECUCION: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_complete_health_check()