"""
Tenable Connection Manager
Version: 2.0.0
Description: Handles secure authentication and session management with Tenable.io API.
"""
import os
from tenable.io import TenableIO

class TenableConnection:
    """
    Manages the lifecycle of the Tenable.io API connection.
    """
    def __init__(self):
        """
        Initializes the connection using environment variables or hardcoded keys.
        Note: Using environment variables is recommended for production.
        """
        self.access_key = 'TU_ACCESS_KEY'
        self.secret_key = 'TU_SECRET_KEY'
        self.client = None

    def get_client(self):
        """
        Creates and returns a TenableIO client instance.
        
        Returns:
            TenableIO: Authenticated API client.
        """
        if not self.client:
            self.client = TenableIO(self.access_key, self.secret_key)
        return self.client