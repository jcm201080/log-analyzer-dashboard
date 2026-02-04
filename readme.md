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
# -------------DASBOARD--------------

## Dashboard de Seguridad

El dashboard de seguridad actúa como punto central de visualización del sistema, permitiendo interpretar de forma clara y rápida los resultados del análisis automático de los registros.

Su diseño prioriza la claridad y evita mostrar información incorrecta o engañosa, adaptándose dinámicamente al tipo de log cargado.

### Comportamiento según el tipo de log

El sistema identifica automáticamente el tipo de log analizado y ajusta el contenido del dashboard en consecuencia:

#### Logs de autenticación (auth)
- Resumen del archivo analizado (líneas totales, analizadas y descartadas).
- Total de intentos de autenticación detectados.
- Usuarios más atacados.
- Hosts/IPs más agresivos.
- Gráfica Top 5 Hosts más agresivos.
- Acceso a exportación de resultados.

#### Logs de red (network)
- Contexto global de red (hosts detectados, eventos totales y hosts críticos).
- Listado de hosts/IPs detectados.
- No se muestran métricas de autenticación ni gráficas asociadas a este tipo de log.

#### Logs no reconocidos (unknown)
- Aviso explícito de tipo de log no soportado.
- El dashboard permanece visible, ocultando automáticamente las secciones que no aplican para evitar confusión.

### Ayudas de interpretación y experiencia de usuario

El dashboard incorpora elementos explicativos, como tooltips y modales informativos, que ayudan a interpretar correctamente los resultados del análisis.

Estas ayudas explican, por ejemplo, la diferencia entre el número total de líneas del archivo y los eventos de seguridad detectados, justificando el filtrado de actividad normal del sistema (ruido) frente a eventos relevantes desde el punto de vista de seguridad.

### Decisiones de diseño

- El dashboard no realiza análisis directo de logs, sino que consume datos ya procesados.
- Las gráficas solo se renderizan cuando existen datos relevantes.
- Se prioriza la interpretación correcta de los resultados frente a la sobrecarga de información.
- La visualización y el análisis se mantienen desacoplados para mejorar mantenibilidad y escalabilidad.


# -------------HOST--------------

## Vista de Hosts Atacantes

La sección de Hosts muestra un listado detallado de las direcciones IP detectadas con actividad sospechosa durante el análisis.

Para cada host se presenta:
- Dirección IP o hostname.
- Información geográfica (país y ciudad cuando está disponible).
- Número de intentos detectados.
- Nivel de gravedad asociado.
- Acceso a una vista de detalle individual.

El sistema diferencia visualmente el tipo de log del que procede cada host (autenticación o red), adaptando el cálculo de la gravedad según el contexto del análisis.


### Detalle del Host

La vista de detalle de un host permite analizar de forma individual una dirección IP concreta, mostrando información contextual y métricas relevantes.

Esta vista facilita el análisis forense y la toma de decisiones, permitiendo entender rápidamente por qué una IP ha sido clasificada como sospechosa.


### Filtros y exportación

La vista de Hosts incluye un filtro temporal a nivel de interfaz, preparado para aplicar rangos de tiempo cuando el log analizado contiene información temporal completa.

Asimismo, se contempla la exportación de listados de IPs sospechosas en formatos CSV y JSON, pensados para su integración con sistemas de seguridad externos como firewalls o IDS/IPS.


# -------------GRÁFICAS--------------

## Gráficas de Seguridad

La sección de Gráficas permite realizar un análisis visual de los patrones de ataque detectados durante el análisis de los registros.

Estas visualizaciones complementan la información mostrada en el dashboard principal, ofreciendo una visión más clara de la distribución y el impacto de los eventos de seguridad.

Las gráficas disponibles incluyen:
- Hosts/IPs más agresivos.
- Usuarios más atacados.
- Origen estimado de los ataques.

La separación entre dashboard y gráficas permite mantener una vista principal clara y delegar el análisis visual detallado en una sección específica.

# -------------EXPORTACIÓN--------------
## Exportación de Inteligencia

El sistema incorpora una sección de exportación orientada a la generación de inteligencia accionable a partir de los resultados del análisis.

Los datos exportables incluyen:
- Direcciones IP identificadas como sospechosas.
- Número de intentos detectados.
- Nivel de riesgo estimado.
- Información estructurada para su integración con sistemas externos.

Se contemplan formatos de exportación como CSV y JSON, pensados para su uso en firewalls, sistemas IDS/IPS o herramientas de análisis y monitorización de seguridad.

La exportación completa se plantea como una fase posterior del proyecto, priorizando en esta etapa la estabilidad, claridad y correcta documentación del sistema.

# -------------SUBIR LOG--------------
## Carga de archivos de log

El sistema permite cargar archivos de log directamente desde la interfaz web para su análisis automático.

El archivo cargado se establece como log activo y es utilizado por todas las vistas del sistema (dashboard, hosts, gráficas y exportación), garantizando coherencia entre los resultados mostrados.

Se admiten logs de sistemas Linux, OpenSSH y formatos similares. En caso de cargar un archivo no reconocido, el sistema informa explícitamente al usuario y adapta la visualización para evitar interpretaciones incorrectas.





# Alcance y estado actual del proyecto

El proyecto se encuentra en una fase funcional y estable, cumpliendo los objetivos definidos para el análisis automático de registros de seguridad.

En esta etapa se ha priorizado:
- La claridad en la visualización de resultados.
- La correcta interpretación de las métricas.
- La separación entre análisis, visualización y exportación.
- La documentación detallada del funcionamiento del sistema.

Las ampliaciones futuras (procesamiento en tiempo real, nuevos formatos de log o sistemas de alertas) quedan planteadas como evoluciones posteriores, sin afectar al núcleo actual del proyecto.


# Estructura del proyecto
## Estructura de directorios

El proyecto se organiza siguiendo una arquitectura modular, separando claramente la lógica de análisis, las rutas de la aplicación web, la presentación visual y los recursos estáticos.

.
├── app.py
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── hosts.py
│   ├── graficas.py
│   ├── export.py
│   ├── upload.py
│   └── funcionamiento.py
├── processing/
│   ├── parser.py
│   ├── analyzer.py
│   ├── geoip.py
│   ├── loader.py
│   └── log_type_detector.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── hosts.html
│   ├── host_detail.html
│   ├── graficas.html
│   ├── export.html
│   ├── upload.html
│   └── funcionamiento.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── data/
│   ├── logs de prueba
│   └── resultados intermedios
└── README.md
## Descripción de los componentes principales

### app.py
Punto de entrada de la aplicación. Inicializa Flask, registra los blueprints y actúa como orquestador del sistema, sin contener lógica de análisis.

### routes/
Contiene las rutas de la aplicación web, organizadas por funcionalidad. Cada archivo gestiona una vista concreta del sistema (dashboard, hosts, gráficas, exportación, carga de logs y documentación).

### processing/
Incluye el núcleo del sistema de análisis. Aquí se realiza el parseo de logs, la detección del tipo de archivo, el análisis de eventos de seguridad y el enriquecimiento de datos.

### templates/
Plantillas HTML encargadas de la presentación visual del sistema. Cada vista consume datos ya procesados y se adapta dinámicamente al tipo de log analizado.

### static/
Recursos estáticos de la aplicación, incluyendo hojas de estilo CSS, scripts JavaScript y recursos gráficos.

### data/
Almacena archivos de log de prueba, datasets utilizados durante el desarrollo y resultados intermedios del análisis.
