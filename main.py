"""
Tenable TVM Health Check Suite - Master Orchestrator
Version: 2.1.0
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
from modules.inventory import InventoryModule
from reports.generator import ReportGenerator

__version__ = "2.1.0"

def run_health_check():
    """Main execution flow."""
    print("\n" + "="*75)
    print(f"      TENABLE TVM HEALTH CHECK - MASTER SUITE v{__version__}")
    print("="*75)
    try:
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        print(f"[*] Starting Professional Audit v{__version__}...")
        
        # 1-8 Audit Modules
        s_res = ScannerHealthModule(tio).run_assessment()
        a_res = AssetHealthModule(tio).run_hygiene_check()
        sc_res = ScanHealthModule(tio).audit_credentials_health()
        u_res = GovernanceModule(tio).get_user_roles_stats()
        r_res = RemediationModule(tio).calculate_sla_performance()
        ri_res = RiskModule(tio).get_top_risk_assets()
        
        from modules.coverage import CoverageModule
        co_res = CoverageModule(tio).analyze_agent_health()
        inv_res = InventoryModule(tio).find_duplicates()

        # Analysis & Reporting
        evaluator = HealthCheckEvaluator()
        final_assessment = evaluator.analyze_all(s_res, a_res, sc_res, u_res, r_res, ri_res, co_res, inv_res)

        reporter = ReportGenerator()
        reporter.save_json_report({"results": final_assessment, "version": __version__})
        reporter.save_txt_summary(final_assessment)

        print("\n" + "-"*33 + " SUMMARY " + "-"*33)
        for item in final_assessment:
            print(f" [{item['status']:<10}] | {item['category']}")
        print("\n" + "="*75 + "\n")

    except Exception as e:
        print(f"\n[!] CRITICAL ERROR: {e}"); sys.exit(1)

if __name__ == "__main__":
    run_health_check()