"""
Report Generator Module - Version: 1.9.0
Description: Ordenamiento alfabetico A-E y restauración de guardado JSON.
"""
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.version = "1.9.0"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pretty_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def _get_strategic_action(self, category, status):
        actions = {
            "INFRAESTRUCTURA": "URGENTE: Restablecer conectividad de scanners. Ver Apendice A.",
            "GOBERNANZA": "REDUCIR RIESGO: Auditar cuentas con privilegios elevados. Ver Apendice B.",
            "PRIORIZACION": "FOCO OPERATIVO: Parchear vulnerabilidades criticas en Apendice C.",
            "INVENTARIO": "OPTIMIZACION: Sanear duplicados y activos obsoletos en Apendice D.",
            "REMEDIACION": "DEUDA TECNICA: Ejecutar remediacion de vulns historicas en Apendice E."
        }
        return actions.get(category, "Mantener monitoreo preventivo.")

    def save_json_report(self, data):
        """Guarda la data cruda en formato JSON para análisis posterior."""
        filename = f"reports/Tenable_HealthCheck_Data_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[+] Datos crudos guardados en: {filename}")

    def save_txt_summary(self, assessment):
        """Genera el reporte maestro TXT con estructura fija A-E."""
        filename = f"reports/HealthCheck_Master_Report_{self.timestamp}.txt"
        
        ordered_categories = ["INFRAESTRUCTURA", "GOBERNANZA", "PRIORIZACION", "INVENTARIO", "REMEDIACION"]
        mapping = {"INFRAESTRUCTURA":"A", "GOBERNANZA":"B", "PRIORIZACION":"C", "INVENTARIO":"D", "REMEDIACION":"E"}

        with open(filename, 'w') as f:
            f.write("="*90 + "\n")
            f.write("       SECCION I: RESUMEN EJECUTIVO DE SALUD TENABLE TVM\n")
            f.write(f"       Fecha de Ejecucion: {self.pretty_date}\n")
            f.write("="*90 + "\n\n")

            for cat_name in ordered_categories:
                item = next((x for x in assessment if x['category'] == cat_name), None)
                if item:
                    f.write(f"[{item['category']}]\n")
                    f.write("-" * 55 + "\n")
                    f.write(f"PRUEBA:      {item['check']}\n")
                    f.write(f"ESTADO:      {item['status']}\n")
                    f.write(f"RESULTADO:   {item['details']}\n")
                    f.write(f"ACCION:      {self._get_strategic_action(item['category'], item['status'])}\n")
                    f.write("." * 55 + "\n\n")

            f.write("\n" + "="*90 + "\n")
            f.write("       SECCION II: APENDICE TECNICO (DETALLE TACTICO PARA OPERACIONES)\n")
            f.write("="*90 + "\n\n")

            for cat_name in ordered_categories:
                item = next((x for x in assessment if x['category'] == cat_name), None)
                letter = mapping.get(cat_name, "X")
                f.write(f"APENDICE {letter}: DETALLE DE {cat_name}\n")
                f.write("-" * 90 + "\n")
                
                if item and item.get('data_for_appendix'):
                    for entry in item['data_for_appendix']:
                        if isinstance(entry, dict):
                            name = str(entry.get('plugin_name', entry.get('name', 'N/A')))
                            clean_name = name.replace("[", "").replace("]", "").replace("'", "")
                            val = entry.get('vpr', entry.get('days_open', ''))
                            label = "VPR" if 'vpr' in entry else "DIAS"
                            asset_info = f" | ASSET: {entry.get('asset', 'N/A')}" if 'asset' in entry else ""
                            f.write(f"    - {clean_name[:45]:<45} | {label}: {val}{asset_info}\n")
                        else:
                            f.write(f"    - {entry}\n")
                else:
                    f.write("    - SIN HALLAZGOS CRITICOS O DATOS QUE REPORTAR EN ESTA CATEGORIA.\n")
                f.write("\n")

            f.write("="*90 + "\n")
            f.write("   FIN DEL INFORME - DOCUMENTO PARA TOMA DE DECISIONES ESTRATEGICAS\n")
            f.write("="*90 + "\n")
        
        print(f"[+] Master Report generado en: {filename}")