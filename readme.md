# Log Analyzer – Análisis Automático de Registros de Seguridad

Se propone el desarrollo de un analizador automático de registros de seguridad basado en Python, capaz de procesar grandes volúmenes de logs de forma eficiente.

El sistema utiliza técnicas de Log Parsing mediante expresiones regulares para extraer información relevante como direcciones IP, usuarios, fechas y tipos de eventos. Posteriormente, emplea librerías de análisis de datos como Pandas para clasificar y detectar patrones de comportamiento sospechoso.

Los resultados se visualizan en un dashboard web que muestra alertas, rankings de orígenes agresivos y métricas clave, permitiendo al equipo técnico una rápida identificación de amenazas sin necesidad de revisar manualmente archivos de registro de gran tamaño.

## Funcionalidades principales
- Lectura eficiente de archivos de log
- Extracción de información crítica mediante RegEx
- Clasificación de ataques por gravedad
- Visualización de resultados en un dashboard web
- Generación automática de una lista de hosts candidatos a bloqueo

## Aplicación práctica
El sistema permite identificar automáticamente los orígenes más agresivos y generar una lista de direcciones candidatas a ser bloqueadas en sistemas de seguridad perimetral como firewalls o sistemas IDS/IPS.

## Fecha
26/12/2025
