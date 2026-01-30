# Tenable TVM Automated Health Check Tool

Version: 1.9.1 (Stable Release)
Python: 3.12
Security: v2-Compliant (Environment Variables)

Esta aplicacion automatiza el proceso de Health Check para Tenable Vulnerability Management (TVM), disenado para consultores y administradores que buscan evaluar la resiliencia y efectividad de un despliegue siguiendo los estandares oficiales de Tenable.

## Estado del Proyecto: v1.9.1
Esta version ha sido certificada como la Linea Base Estable. Se ha optimizado la logica de filtrado de la API v3 y se ha implementado un sistema de gestion de credenciales mediante variables de entorno para maxima seguridad y cumplimiento.

## Alcance del Proyecto
La herramienta automatiza las tareas clave de la Actividad 2: Solution Review del Services Brief:
- Infraestructura: Analisis de salud (Online/Offline) y actualizacion de scanners.
- Higiene de Activos: Identificacion de activos stale para optimizar licenciamiento.
- Gobernanza (RBAC): Auditoria de roles y permisos de usuarios.
- Remediacion (SLA): Calculo de deuda tecnica y cumplimiento de tiempos de parcheo.
- Priorizacion (VPR): Inteligencia sobre activos de mayor riesgo.
- Inventario: Deteccion de duplicados y optimizacion de base de datos.

## Arquitectura Modular
- core/: Gestion de conexion reutilizable y carga segura mediante .env.
- modules/: Logica de diagnostico independiente para 8 pilares criticos de la plataforma.
- reports/: Generacion de entregables en JSON (datos crudos) y TXT (resumen ejecutivo).

## Instalacion y Configuracion

1. Clonar el Repositorio:
   git clone https://github.com/jmanueloporto/tenable-tvm-healthcheck.git
   cd tenable-tvm-healthcheck

2. Crear el Entorno Virtual:
   python3 -m venv tenable
   source tenable/bin/activate
   pip install -r requirements.txt

3. Configurar la Seguridad (.env):
   Crea un archivo .env en la raiz del proyecto para almacenar las API Keys de forma segura.
   TENABLE_ACCESS_KEY=your_access_key
   TENABLE_SECRET_KEY=your_secret_key

## Ejecucion
Para iniciar el proceso de Health Check y generar los reportes de evaluacion:
python3 main.py

## Entregables
Al finalizar, la herramienta genera:
- Assessment Report (JSON): Hallazgos detallados para analisis de datos y trazabilidad.
- Executive Summary (TXT): Resumen de semaforizacion (Optimal/Critical) para la toma de decisiones gerenciales.

---
Nota: Este proyecto es una herramienta de asistencia para consultoria y debe ser utilizado bajo el cumplimiento de los acuerdos de licencia de Tenable.
