import os
import requests
from tenable.io import TenableIO

class TenableConnection:
    def __init__(self):
        self.access_key = '0a025fe8b323d25bdc4b2ed4c45ddbd309a0bbc671eb91cdf9f2fa4576cabcc4'
        self.secret_key = '3e2c46dbc78aff20f712a5ef1528ca9373ccb21c6e8ee7e7e7ed7775303206e0'

    def get_client(self):
        return TenableIO(self.access_key, self.secret_key)
