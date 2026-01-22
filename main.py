"""
Tenable TVM Health Check Suite
Version: 1.7
Description: Orquestador integral con analisis de cobertura de agentes.
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
from reports.generator import ReportGenerator

__version__ = "1.7"

def run_health_check():
    print("\n" + "="*75)
    print(f"      TENABLE TVM HEALTH CHECK - FULL SUITE v{__version__}")
    print("="*75)
    
    try:
        api_manager = TenableConnection()
        tio = api_manager.get_client()

        print(f"[*] Iniciando Auditoria v{__version__}...")

        print("[*] 1/7 Analizando Infraestructura...")
        s_results = ScannerHealthModule(tio).run_assessment()
        
        print("[*] 2/7 Analizando Higiene de Activos...")
        a_results = AssetHealthModule(tio).run_hygiene_check()
        
        print("[*] 3/7 Auditando Calidad de Escaneo...")
        scan_results = ScanHealthModule(tio).audit_credentials_health()
        
        print("[*] 4/7 Evaluando Gobernanza (RBAC)...")
        u_results = GovernanceModule(tio).get_user_roles_stats()

        print("[*] 5/7 Calculando SLA de Remediacion...")
        r_results = RemediationModule(tio).calculate_sla_performance()

        print("[*] 6/7 Identificando Activos Criticos (VPR)...")
        risk_results = RiskModule(tio).get_top_risk_assets()

        print("[*] 7/7 Analizando Cobertura de Agentes...")
        cov_results = CoverageModule(tio).analyze_agent_health()

        # Evaluación Integral
        evaluator = HealthCheckEvaluator()
        final_assessment = evaluator.analyze_all(s_results, a_results, scan_results, u_results, r_results, risk_results, cov_results)

        # Reportes
        reporter = ReportGenerator()
        reporter.save_json_report({"results": final_assessment, "version": __version__})
        reporter.save_txt_summary(final_assessment)

        print("\n" + "-"*33 + " RESULTADOS " + "-"*33)
        for item in final_assessment:
            tag = f"[{item['status']}]"
            print(f" {tag:<15} | {item['category']}: {item['check']}")

        print("\n" + "="*75)
        print(f"INFORME v{__version__} GENERADO CORRECTAMENTE")
        print("="*75 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR CRITICO EN v{__version__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_health_check()