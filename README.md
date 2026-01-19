# Tenable TVM Automated Health Check Tool

Esta aplicación automatiza el proceso de Health Check para Tenable Vulnerability Management (TVM), diseñado para consultores que buscan evaluar la resiliencia y efectividad de un despliegue siguiendo los estándares oficiales de Tenable.

## Alcance del Proyecto
La herramienta automatiza las tareas clave de la Actividad 2: Solution Review del Services Brief:
- Evaluacion de Infraestructura: Analisis del estado de salud (Online/Offline), rendimiento y actualizacion de los scanners de red.
- Higiene de Activos: Identificacion de activos stale o inactivos para optimizar el licenciamiento y el almacenamiento de la plataforma.
- Auditoria de Escaneos: Revision de la configuracion, estado de finalizacion y efectividad de las politicas de escaneo.

## Requisitos Tecnicos
- Sistema Operativo: Linux Mint (o distribuciones basadas en Debian/Ubuntu).
- Lenguaje: Python 3.x.
- Librerias principales: pyTenable, python-dotenv, pandas.

## Instalacion y Configuracion

1. Clonar el Repositorio:
   git clone https://github.com/tu-usuario/tenable-tvm-healthcheck.git
   cd tenable-tvm-healthcheck

2. Crear el Entorno Virtual:
   python3 -m venv tenable
   source tenable/bin/activate
   pip install -r requirements.txt

3. Configurar la Seguridad (.env):
   Crea un archivo .env en la raiz del proyecto para almacenar las API Keys. Este archivo esta excluido del control de versiones por el archivo .gitignore.
   TENABLE_ACCESS_KEY=TU_ACCESS_KEY_AQUI
   TENABLE_SECRET_KEY=TU_SECRET_KEY_AQUI

## Arquitectura Modular
- core/: Gestiona la conexion reutilizable y la carga segura de credenciales mediante variables de entorno.
- modules/: Contiene la logica de diagnostico independiente para scanners, activos y politicas.
- reports/: Genera los entregables tecnicos en formato JSON para el analisis de hallazgos.

## Ejecucion
Para iniciar el proceso de Health Check y generar los reportes de evaluacion:
python3 main.py

## Entregables
Al finalizar, la herramienta genera un Assessment Report que identifica:
- Brechas (Gaps) en la configuracion y el rendimiento de la solucion.
- Datos cuantitativos para la toma de decisiones sobre higiene de activos.
- Inventario detallado del estado de la infraestructura de escaneo.

---
Nota: Este proyecto es una herramienta de asistencia para consultoria y debe ser utilizado bajo el cumplimiento de los acuerdos de licencia de Tenable.
