import sys
from core.connection import TenableConnection
from core.evaluator import HealthCheckEvaluator
from modules.scanners import ScannerHealthModule
from modules.assets import AssetHealthModule
from modules.scans import ScanHealthModule
from modules.governance import GovernanceModule # Importacion nueva
from reports.generator import ReportGenerator

def run_health_check_v2():
    print("\n" + "="*60)
    print("      TENABLE HEALTH CHECK - VERSION DE CONSULTORIA")
    print("="*60)
    
    try:
        # 1. Conexion
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        # 2. Diagnosticos
        print("[*] Recolectando telemetria de Infraestructura y Activos...")
        s_results = ScannerHealthModule(tio).run_assessment()
        a_results = AssetHealthModule(tio).run_hygiene_check()
        
        print("[*] Analizando calidad de escaneos...")
        scan_results = ScanHealthModule(tio).audit_credentials_health()
        
        print("[*] Auditando usuarios y roles (RBAC)...")
        u_results = GovernanceModule(tio).get_user_roles_stats()

        # 3. Evaluacion Integral
        print("[*] Procesando informe consolidado...")
        evaluator = HealthCheckEvaluator()
        final_assessment = evaluator.analyze_all(s_results, a_results, scan_results, u_results)

        # 4. Generacion de Entregables
        reporter = ReportGenerator()
        reporter.save_json_report({"results": final_assessment})
        reporter.save_txt_summary(final_assessment)

        # 5. Resumen Visual
        print("\nRESUMEN DE ESTADOS:")
        for item in final_assessment:
            status_tag = f"[{item['status']}]"
            print(f" {status_tag:<15} | {item['category']}: {item['check']}")

        print("\n" + "="*60)
        print("EL REPORTE HA SIDO GENERADO CON EXITO")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR EN EL PROCESO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_health_check_v2()