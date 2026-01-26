"""
Professional Report Generator
Version: 2.1.0
"""
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.version = "2.1.0"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pretty_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def _get_strategic_action(self, category, status):
        actions = {
            "INFRASTRUCTURE": "URGENTE: Restore scanner connectivity. See Appendix A.",
            "GOVERNANCE": "REDUCE RISK: Audit accounts with elevated privileges. See Appendix B.",
            "PRIORITIZATION": "OPERATIONAL FOCUS: Patch high-VPR vulnerabilities. See Appendix C.",
            "INVENTORY": "OPTIMIZATION: Clean up duplicate assets. See Appendix D.",
            "REMEDIATION": "TECHNICAL DEBT: Remediate critical historical vulns. See Appendix E."
        }
        return actions.get(category, "Maintain monitoring.")

    def save_json_report(self, data):
        filename = f"reports/HealthCheck_Data_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[+] Raw data saved to: {filename}")

    def save_txt_summary(self, assessment):
        filename = f"reports/Master_Health_Report_{self.timestamp}.txt"
        order = ["INFRASTRUCTURE", "GOVERNANCE", "PRIORITIZATION", "INVENTORY", "REMEDIATION"]
        mapping = {"INFRASTRUCTURE":"A", "GOVERNANCE":"B", "PRIORITIZATION":"C", "INVENTORY":"D", "REMEDIATION":"E"}

        with open(filename, 'w') as f:
            f.write("="*90 + "\n")
            f.write("       SECTION I: EXECUTIVE SUMMARY - TENABLE TVM\n")
            f.write(f"       Date: {self.pretty_date}\n")
            f.write("="*90 + "\n\n")

            for cat in order:
                item = next((x for x in assessment if x['category'] == cat), None)
                if item:
                    f.write(f"[{item['category']}]\n")
                    f.write(f"STATUS:      {item['status']}\n")
                    f.write(f"RESULT:      {item['details']}\n")
                    f.write(f"ACTION:      {self._get_strategic_action(item['category'], item['status'])}\n")
                    f.write("." * 55 + "\n\n")

            f.write("\n" + "="*90 + "\n")
            f.write("       SECTION II: TECHNICAL APPENDICES\n")
            f.write("="*90 + "\n\n")

            for cat in order:
                item = next((x for x in assessment if x['category'] == cat), None)
                letter = mapping.get(cat, "X")
                f.write(f"APPENDIX {letter}: {cat} DETAILS\n")
                f.write("-" * 90 + "\n")
                if item and item.get('data_for_appendix'):
                    for entry in item['data_for_appendix']:
                        f.write(f"    - {entry}\n")
                else:
                    f.write("    - NO CRITICAL FINDINGS.\n")
                f.write("\n")