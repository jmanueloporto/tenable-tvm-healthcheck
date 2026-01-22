"""
Tenable TVM Health Check Suite
Version: 1.8
Description: Orquestador final con 8 pasos de auditoria.
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

__version__ = "1.8"

def run_health_check():
    print("\n" + "="*75)
    print(f"      TENABLE TVM HEALTH CHECK - FULL SUITE v{__version__}")
    print("="*75)
    try:
        tio = TenableConnection().get_client()
        print(f"[*] Iniciando Auditoria Final v{__version__}...")

        s_res = ScannerHealthModule(tio).run_assessment()
        a_res = AssetHealthModule(tio).run_hygiene_check()
        sc_res = ScanHealthModule(tio).audit_credentials_health()
        u_res = GovernanceModule(tio).get_user_roles_stats()
        r_res = RemediationModule(tio).calculate_sla_performance()
        ri_res = RiskModule(tio).get_top_risk_assets()
        co_res = CoverageModule(tio).analyze_agent_health()
        inv_res = InventoryModule(tio).find_duplicates()

        evaluator = HealthCheckEvaluator()
        final_assessment = evaluator.analyze_all(s_res, a_res, sc_res, u_res, r_res, ri_res, co_res, inv_res)

        ReportGenerator().save_json_report({"results": final_assessment, "version": __version__})
        ReportGenerator().save_txt_summary(final_assessment)

        print("\n" + "-"*33 + " RESULTADOS " + "-"*33)
        for item in final_assessment:
            print(f" [{item['status']:<10}] | {item['category']}: {item['check']}")
        print("\n" + "="*75 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR: {e}"); sys.exit(1)

if __name__ == "__main__": run_health_check()