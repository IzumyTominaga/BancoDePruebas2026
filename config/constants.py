"""Constantes globales del sistema de telemetría de banco de pruebas Horus."""

import os

# Constantes físicas y de cálculo de propulsión
GRAVITY: float = 9.80665
"""Aceleración de la gravedad estándar en m/s² para conversión entre Newtons y kilogramos-fuerza."""

THRUST_THRESHOLD: float = 2.0
"""Umbral de empuje en Newtons para filtrar ruido de la celda de carga e iniciar integración de impulso."""

# Parámetros de comunicación serie
DEFAULT_BAUDRATE: int = 115200
"""Velocidad en baudios por defecto para la interfaz serie."""

RECONNECT_INTERVAL_MS: int = 3000
"""Intervalo de espera en milisegundos para reintentar la conexión serie."""

# Modos de comunicación
MODE_CABLE: str = "cable"
"""Modo de enlace alámbrico mediante cable directo o RS-485."""

MODE_LORA: str = "lora"
"""Modo de enlace inalámbrico de largo alcance LoRa."""

# Tamaños de paquetes de datos binarios (en bytes)
PACKET_SIZE_CABLE: int = 8
"""Tamaño de paquete binario en modo cable: float (4B) empuje + uint32 (4B) secuencia = 8 bytes."""

PACKET_SIZE_LORA: int = 9
"""Tamaño de paquete binario en modo LoRa: float (4B) empuje + uint32 (4B) secuencia + int8 (1B) rssi = 9 bytes."""

# Archivo de configuración
CONFIG_FILE: str = os.path.join(os.path.expanduser("~"), ".horus_config.json")
"""Ruta al archivo de configuración de usuario en formato JSON."""

# Paleta de colores temáticos de la interfaz (Dark Aerospace Theme)
THEME_BG: str = "#0d0d1a"
"""Color de fondo principal de la aplicación."""

THEME_CYAN: str = "#00e5ff"
"""Color cyan primario para telemetría activa y empuje instantáneo."""

THEME_GREEN: str = "#00ff88"
"""Color verde para estados conectados, impulso acumulado y botón de inicio."""

THEME_RED: str = "#ff4444"
"""Color rojo para estados desconectados, botones de parada y fuego."""

THEME_ORANGE: str = "#ff9800"
"""Color naranja para empuje máximo y estados de advertencia."""

THEME_PINK: str = "#ff4488"
"""Color rosa/magenta para la clasificación de motor NAR."""

THEME_PURPLE: str = "#aa88ff"
"""Color púrpura para telemetría LoRa e intensidad de señal RSSI."""

THEME_WARN_ORANGE: str = "#ff6644"
"""Color naranja cálido para métricas de paquetes perdidos."""

# Colores secundarios para componentes UI
THEME_PANEL_BG: str = "#1a1a2e"
"""Color de fondo para tarjetas de métricas (KpiCard) y paneles secundarios."""

THEME_BUTTON_BG: str = "#1e1e2e"
"""Color de fondo predeterminado de botones."""

THEME_BORDER: str = "#333355"
"""Color de bordes de controles y marcos de ventana."""

THEME_TEXT_MUTED: str = "#cccccc"
"""Color de texto secundario y etiquetas informativas."""
