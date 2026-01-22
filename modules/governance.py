"""
Governance & RBAC Module
Version: 1.5
Description: Auditoria de usuarios y roles basada en IDs de Tenable.
"""

class GovernanceModule:
    def __init__(self, tio_client):
        self.version = "1.5"
        self.tio = tio_client
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
                perm_id = str(user.get('permissions') or user.get('user_role') or "0")
                role_name = self.ROLE_MAP.get(perm_id, f"Custom_ID_{perm_id}")
                user_stats[role_name] = user_stats.get(role_name, 0) + 1
                
            return {"total_users": len(users), "breakdown": user_stats}
        except Exception:
            return {"total_users": 0, "breakdown": {}}