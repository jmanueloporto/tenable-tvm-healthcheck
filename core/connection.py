import os
import requests
from tenable.io import TenableIO

class TenableConnection:
    """
    A class to manage connection to the Tenable.io API.
    
    This class handles authentication and provides a client object
    for interacting with Tenable.io services using the provided
    access and secret keys.
    """
    
    def __init__(self):
        """
        Initializes the TenableConnection with API credentials.
        
        The constructor sets up the access and secret keys required
        for authenticating with the Tenable.io API. These credentials
        should have appropriate permissions for the intended API operations.
        """
        self.access_key = '0a025fe8b323d25bdc4b2ed4c45ddbd309a0bbc671eb91cdf9f2fa4576cabcc4'
        self.secret_key = '3e2c46dbc78aff20f712a5ef1528ca9373ccb21c6e8ee7e7e7ed7775303206e0'
    
    def get_client(self):
        """
        Creates and returns a Tenable.io client instance.
        
        This method initializes and returns a TenableIO client object
        using the stored access and secret keys. The client can be used
        to make various API calls to Tenable.io services.
        
        Returns:
            TenableIO: An authenticated Tenable.io client instance
            
        Example:
            >>> connection = TenableConnection()
            >>> client = connection.get_client()
            >>> # Now use client to make API calls
        """
        return TenableIO(self.access_key, self.secret_key)