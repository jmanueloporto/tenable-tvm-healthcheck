"""
Agent Coverage Module
Version: 1.7
Description: Analiza la distribucion de Nessus Agents y detecta activos sin cobertura.
"""

class CoverageModule:
    def __init__(self, tio_client):
        self.version = "1.7"
        self.tio = tio_client

    def analyze_agent_health(self):
        """
        Analiza el estado de los agentes en el tenant.
        """
        stats = {"total_agents": 0, "online": 0, "offline": 0, "unlinked": 0}
        try:
            # Obtenemos la lista de agentes
            agents = self.tio.agents.list()
            for agent in agents:
                stats["total_agents"] += 1
                status = agent.get('status', '').lower()
                if status == 'on-line': stats["online"] += 1
                elif status == 'off-line': stats["offline"] += 1
                else: stats["unlinked"] += 1
            
            return stats
        except Exception as e:
            print(f"Error en CoverageModule: {e}")
            return stats