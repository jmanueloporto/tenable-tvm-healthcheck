"""
Tenable TVM Health Check Suite - Version: 1.9.0
"""
import sys
from core.connection import TenableConnection
from core.evaluator import HealthCheckEvaluator
from modules.scanners import ScannerHealthModule
from modules.assets import AssetHealthModule
from modules.scans import ScanHealthModule
from modules.governance import GovernanceModule
from modules.remediation import RemediationModule
from modules.risk import RiskModule
from modules.coverage import CoverageModule
from modules.inventory import InventoryModule
from reports.generator import ReportGenerator

__version__ = "1.9.0"

def run_health_check():
    print("\n" + "="*75)
    print(f"      TENABLE TVM HEALTH CHECK - MASTER SUITE v{__version__}")
    print("="*75)
    try:
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        print(f"[*] 1/8 Analizando Infraestructura de Scanners...")
        s_res = ScannerHealthModule(tio).run_assessment()
        
        print("[*] 2/8 Analizando Higiene de Activos...")
        a_res = AssetHealthModule(tio).run_hygiene_check()
        
        print("[*] 3/8 Auditando Calidad de Escaneo...")
        sc_res = ScanHealthModule(tio).audit_credentials_health()
        
        print("[*] 4/8 Evaluando Gobernanza (RBAC)...")
        u_res = GovernanceModule(tio).get_user_roles_stats()
        
        print("[*] 5/8 Calculando SLA y Deuda Tecnica...")
        r_res = RemediationModule(tio).calculate_sla_performance()
        
        print("[*] 6/8 Identificando Inteligencia VPR...")
        ri_res = RiskModule(tio).get_top_risk_assets()
        
        print("[*] 7/8 Analizando Cobertura de Agentes...")
        co_res = CoverageModule(tio).analyze_agent_health()
        
        print("[*] 8/8 Buscando Duplicados...")
        inv_res = InventoryModule(tio).find_duplicates()

        evaluator = HealthCheckEvaluator()
        final_assessment = evaluator.analyze_all(s_res, a_res, sc_res, u_res, r_res, ri_res, co_res, inv_res)

        reporter = ReportGenerator()
        reporter.save_json_report({"results": final_assessment, "version": __version__})
        reporter.save_txt_summary(final_assessment)

        print("\n" + "-"*33 + " RESUMEN " + "-"*33)
        for item in final_assessment:
            print(f" [{item['status']:<10}] | {item['category']}")
        print("\n" + "="*75 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR CRITICO: {e}"); sys.exit(1)

if __name__ == "__main__":
    run_health_check()