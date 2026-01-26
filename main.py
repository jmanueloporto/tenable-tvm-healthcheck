"""
Tenable TVM Health Check Suite - Master Orchestrator
Version: 2.0.0
Description: Main entry point that coordinates data extraction, analysis, and reporting.
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

__version__ = "2.0.0"

def run_health_check():
    """
    Orchestrates the full audit process across all specialized modules.
    """
    print("\n" + "="*75)
    print(f"      TENABLE TVM HEALTH CHECK - MASTER SUITE v{__version__}")
    print("="*75)
    try:
        # Initialize API Connection
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        print(f"[*] Starting Professional Audit v{__version__}...")
        
        print("[*] 1/8 Analyzing Scanner Infrastructure...")
        s_res = ScannerHealthModule(tio).run_assessment()
        
        print("[*] 2/8 Analyzing Asset Hygiene...")
        a_res = AssetHealthModule(tio).run_hygiene_check()
        
        print("[*] 3/8 Auditing Scan Quality (Credentials)...")
        sc_res = ScanHealthModule(tio).audit_credentials_health()
        
        print("[*] 4/8 Evaluating Governance (RBAC)...")
        u_res = GovernanceModule(tio).get_user_roles_stats()
        
        print("[*] 5/8 Calculating SLA and Technical Debt...")
        r_res = RemediationModule(tio).calculate_sla_performance()
        
        print("[*] 6/8 Identifying VPR Intelligence...")
        ri_res = RiskModule(tio).get_top_risk_assets()
        
        print("[*] 7/8 Analyzing Agent Coverage...")
        # Note: CoverageModule logic assumed similar to others
        from modules.coverage import CoverageModule
        co_res = CoverageModule(tio).analyze_agent_health()
        
        print("[*] 8/8 Finding Inventory Duplicates...")
        inv_res = InventoryModule(tio).find_duplicates()

        # Data Analysis and Evaluation
        evaluator = HealthCheckEvaluator()
        final_assessment = evaluator.analyze_all(s_res, a_res, sc_res, u_res, r_res, ri_res, co_res, inv_res)

        # Report Generation
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