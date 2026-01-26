"""
Professional Report Generator
Version: 2.0.0
Description: Produces structured executive and technical reports in English.
"""
import json
from datetime import datetime

class ReportGenerator:
    """
    Handles file output for JSON data and human-readable TXT reports.
    """
    def __init__(self):
        self.version = "2.0.0"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pretty_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def _get_strategic_action(self, category, status):
        """Returns a professional recommendation based on category status."""
        actions = {
            "INFRASTRUCTURE": "URGENT: Restore scanner connectivity. See Appendix A.",
            "GOVERNANCE": "REDUCE RISK: Audit accounts with elevated privileges. See Appendix B.",
            "PRIORITIZATION": "OPERATIONAL FOCUS: Patch critical vulnerabilities. See Appendix C.",
            "INVENTORY": "OPTIMIZATION: Clean up duplicate and obsolete assets. See Appendix D.",
            "REMEDIATION": "TECHNICAL DEBT: Remediate historical vulnerabilities. See Appendix E."
        }
        return actions.get(category, "Maintain preventive monitoring.")

    def save_json_report(self, data):
        filename = f"reports/Tenable_HealthCheck_Data_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[+] Raw data saved to: {filename}")

    def save_txt_summary(self, assessment):
        filename = f"reports/HealthCheck_Master_Report_{self.timestamp}.txt"
        order = ["INFRASTRUCTURE", "GOVERNANCE", "PRIORITIZATION", "INVENTORY", "REMEDIATION"]
        mapping = {"INFRASTRUCTURE":"A", "GOVERNANCE":"B", "PRIORITIZATION":"C", "INVENTARIO":"D", "REMEDIACION":"E"}

        with open(filename, 'w') as f:
            f.write("="*90 + "\n")
            f.write("       SECTION I: EXECUTIVE SUMMARY - TENABLE TVM HEALTH\n")
            f.write(f"       Execution Date: {self.pretty_date}\n")
            f.write("="*90 + "\n\n")

            for cat in order:
                item = next((x for x in assessment if x['category'] == cat), None)
                if item:
                    f.write(f"[{item['category']}]\n")
                    f.write("-" * 55 + "\n")
                    f.write(f"CHECK:       {item['check']}\n")
                    f.write(f"STATUS:      {item['status']}\n")
                    f.write(f"RESULT:      {item['details']}\n")
                    f.write(f"ACTION:      {self._get_strategic_action(item['category'], item['status'])}\n")
                    f.write("." * 55 + "\n\n")

            f.write("\n" + "="*90 + "\n")
            f.write("       SECTION II: TECHNICAL APPENDIX (OPERATIONAL DETAILS)\n")
            f.write("="*90 + "\n\n")

            for cat in order:
                item = next((x for x in assessment if x['category'] == cat), None)
                letter = mapping.get(cat, "X")
                f.write(f"APPENDIX {letter}: {cat} DETAILS\n")
                f.write("-" * 90 + "\n")
                
                if item and item.get('data_for_appendix'):
                    for entry in item['data_for_appendix']:
                        if isinstance(entry, dict):
                            name = str(entry.get('plugin_name', entry.get('name', 'N/A')))
                            clean_name = name.replace("[", "").replace("]", "").replace("'", "")
                            val = entry.get('vpr', entry.get('days_open', ''))
                            label = "VPR" if 'vpr' in entry else "DAYS"
                            asset = f" | ASSET: {entry.get('asset', 'N/A')}" if 'asset' in entry else ""
                            f.write(f"    - {clean_name[:45]:<45} | {label}: {val}{asset}\n")
                        else:
                            f.write(f"    - {entry}\n")
                else:
                    f.write("    - NO CRITICAL FINDINGS DETECTED IN THIS CATEGORY.\n")
                f.write("\n")

            f.write("="*90 + "\n")
            f.write("   END OF REPORT - DECISION-MAKING STRATEGIC DOCUMENT\n")
            f.write("="*90 + "\n")