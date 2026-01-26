"""
Core Evaluator Module
Version: 2.0.0
Description: Translates raw technical data into executive business health status.
"""
class HealthCheckEvaluator:
    """
    Analyzes module results to determine the overall security posture.
    """
    def __init__(self):
        self.version = "2.0.0"

    def analyze_all(self, s_res, a_res, sc_res, u_res, r_res, ri_res, co_res, inv_res):
        """
        Maps technical results to professional categories.
        
        Returns:
            list: Dictionaries containing status, details, and appendix data.
        """
        return [
            {
                "category": "INFRASTRUCTURE",
                "check": "Scanner Availability",
                "status": "CRITICAL" if s_res['stats']['offline'] > 0 else "OPTIMAL",
                "details": f"Total: {s_res['stats'].get('total',0)}, Offline: {s_res['stats'].get('offline',0)}.",
                "data_for_appendix": s_res.get('offline_list', [])
            },
            {
                "category": "GOVERNANCE",
                "check": "Role Distribution (RBAC)",
                "status": "CRITICAL" if u_res['breakdown'].get('Administrator', 0) > 5 else "OPTIMAL",
                "details": f"Total Users: {u_res.get('total_users',0)}. Admins: {u_res['breakdown'].get('Administrator', 0)}.",
                "data_for_appendix": u_res.get('admin_list', [])
            },
            {
                "category": "PRIORITIZATION",
                "check": "Predictive Risk (VPR Intelligence)",
                "status": "CRITICAL" if any(x.get('vpr', 0) > 8.0 for x in ri_res) else "OPTIMAL",
                "details": f"Critical VPR findings analyzed: {len(ri_res)}.",
                "data_for_appendix": ri_res
            },
            {
                "category": "INVENTORY",
                "check": "Hygiene & Licensing",
                "status": "OPTIMAL" if inv_res.get('duplicate_count', 0) == 0 else "WARNING",
                "details": f"Duplicates: {inv_res.get('duplicate_count', 0)}. Stale (>90d): {a_res['stats'].get('stale_assets', 0)}.",
                "data_for_appendix": inv_res.get('list', [])
            },
            {
                "category": "REMEDIATION",
                "check": "SLA & Technical Debt",
                "status": "CRITICAL" if r_res['avg_days_open'] > 60 else "OPTIMAL",
                "details": f"Avg: {r_res['avg_days_open']} days. Overdue Criticals: {r_res['overdue_criticals']}.",
                "data_for_appendix": r_res.get('oldest_vulns', [])
            }
        ]