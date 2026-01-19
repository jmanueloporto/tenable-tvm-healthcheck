import os
from tenable.io import TenableIO
from dotenv import load_dotenv

# Carga las credenciales del archivo .env que está en la raíz del proyecto
load_dotenv()

class TenableConnection:
    """
    Módulo Core para gestionar la conexión reutilizable con TVM.
    Garantiza que el consultor tenga acceso a los recursos necesarios.
    """
    def __init__(self):
        # Recupera las llaves del entorno de forma segura
        self.access_key = os.getenv('TENABLE_ACCESS_KEY')
        self.secret_key = os.getenv('TENABLE_SECRET_KEY')
        
        # Validación de requisitos: el cliente debe proporcionar acceso con privilegios [cite: 65]
        if not self.access_key or not self.secret_key:
            raise EnvironmentError(
                "Error: No se detectaron las API Keys. "
                "Revisa el archivo .env en la raíz del proyecto."
            )

        # Inicializa la conexión oficial identificada como herramienta de consultoría
        self.tio = TenableIO(
            self.access_key, 
            self.secret_key, 
            vendor='Consultancy_Project', 
            product='Auto_HealthCheck_Tool'
        )

    def get_client(self):
        """Retorna el cliente de API para ser usado en los módulos de diagnóstico."""
        return self.tio