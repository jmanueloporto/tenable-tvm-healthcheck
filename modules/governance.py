"""
Governance Module - Version: 1.8.6
"""
class GovernanceModule:
    def __init__(self, tio_client):
        self.tio = tio_client

    def get_user_roles_stats(self):
        users = self.tio.users.list()
        admin_list = []
        breakdown = {"Administrator": 0}
        
        for u in users:
            role = u.get('role_name')
            if role == 'Administrator':
                breakdown["Administrator"] += 1
                admin_list.append(f"USUARIO: {u.get('username'):<20} | EMAIL: {u.get('email')}")
            
        return {
            "total_users": len(users),
            "breakdown": breakdown,
            "admin_list": sorted(admin_list)
        }