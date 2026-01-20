class GovernanceModule:
    """
    Analiza la configuracion de usuarios y roles (RBAC).
    Mapeo ajustado segun los IDs reales observados en el reporte del cliente.
    """
    def __init__(self, tio_client):
        self.tio = tio_client
        # Mapeo oficial de Tenable.io observado en el CSV
        self.ROLE_MAP = {
            "64": "Administrator",
            "40": "Security Manager",
            "32": "Standard",
            "24": "Scan Operator",
            "16": "Basic",
            "0": "No Access / Deactivated"
        }

    def get_user_roles_stats(self):
        user_stats = {}
        try:
            users = self.tio.users.list()
            
            for user in users:
                # Extraemos el valor del campo 'permissions' que es el que viene en el CSV
                # pyTenable a veces lo mapea como 'permissions' o 'user_role'
                perm_id = str(user.get('permissions') or user.get('user_role') or "0")
                
                # Traducimos usando el mapa corregido
                role_name = self.ROLE_MAP.get(perm_id, f"Custom_ID_{perm_id}")
                
                user_stats[role_name] = user_stats.get(role_name, 0) + 1
                
            return {
                "total_users": len(users),
                "breakdown": user_stats
            }
        except Exception as e:
            return {"total_users": 0, "breakdown": {}, "error": str(e)}