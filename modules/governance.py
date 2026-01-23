"""
Governance Module - Version: 1.8.7
"""
class GovernanceModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def get_user_roles_stats(self):
        users = self.tio.users.list()
        admin_list = []
        breakdown = {"Administrator": 0}
        
        for u in users:
            role = str(u.get('role_name', '')).lower()
            if 'admin' in role:
                breakdown["Administrator"] += 1
                admin_list.append(f"USUARIO: {u.get('username'):<25} | ROL: {role.upper()}")
            
        return {
            "total_users": len(users),
            "breakdown": breakdown,
            "admin_list": sorted(admin_list)
        }