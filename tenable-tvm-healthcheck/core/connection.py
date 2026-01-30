"""
Tenable Connection Manager
Version: 2.1.0
Description: Securely handles API authentication using environment variables.
"""
import os
from dotenv import load_dotenv
from tenable.io import TenableIO

# Load variables from the local .env file
load_dotenv()

class TenableConnection:
    """
    Manages the lifecycle of the Tenable.io API connection.
    """
    def __init__(self):
        """
        Initializes credentials from environment variables.
        """
        self.access_key = os.getenv('TENABLE_ACCESS_KEY')
        self.secret_key = os.getenv('TENABLE_SECRET_KEY')
        self.client = None

    def get_client(self):
        """
        Returns an authenticated TenableIO client.
        
        Raises:
            ValueError: If API keys are missing from the environment.
        """
        if not self.access_key or not self.secret_key:
            raise ValueError(
                "CRITICAL ERROR: API Keys missing. Check your .env file "
                "and ensure TENABLE_ACCESS_KEY and TENABLE_SECRET_KEY are set."
            )
            
        if not self.client:
            self.client = TenableIO(self.access_key, self.secret_key)
        return self.client