"""
Governance & RBAC Module
Version: 2.0.0
Description: Audits user roles and administrative privileges for security compliance.
"""
class GovernanceModule:
    """
    Reviews user accounts and their assigned roles in the platform.
    """
    def __init__(self, tio_client):
        self.tio = tio_client

    def get_user_roles_stats(self):
        """
        Lists users and flags those with 'Administrator' privileges.
        
        Returns:
            dict: Breakdown of roles and list of administrators for Appendix B.
        """
        users = self.tio.users.list()
        admin_list = []
        role_breakdown = {}

        for user in users:
            role = user.get('role_name', 'None')
            role_breakdown[role] = role_breakdown.get(role, 0) + 1
            
            if role == 'Administrator':
                admin_list.append(f"USER: {user.get('username'):<30} | EMAIL: {user.get('email')}")

        return {
            "total_users": len(users),
            "breakdown": role_breakdown,
            "admin_list": admin_list
        }