"""Estilos visuales y hojas de estilo QSS centralizadas para la aplicación Horus Telemetry."""

from config.constants import (
    THEME_BG,
    THEME_BORDER,
    THEME_BUTTON_BG,
    THEME_CYAN,
    THEME_GREEN,
    THEME_PANEL_BG,
    THEME_RED,
    THEME_TEXT_MUTED,
)

MAIN_STYLESHEET: str = f"""
QMainWindow, QWidget {{
    background: {THEME_BG};
}}
QLabel {{
    color: {THEME_TEXT_MUTED};
    font-family: 'Courier New', monospace;
}}
QPushButton {{
    background: {THEME_BUTTON_BG};
    color: #dddddd;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    font-family: 'Courier New', monospace;
    border: 1px solid {THEME_BORDER};
}}
QPushButton:hover {{
    background: #2a2a3e;
    border-color: #5555aa;
}}
QPushButton:pressed {{
    background: #111122;
}}
QComboBox {{
    background: {THEME_BUTTON_BG};
    color: #dddddd;
    padding: 6px;
    border: 1px solid {THEME_BORDER};
    font-family: 'Courier New', monospace;
}}
"""
"""Hoja de estilo principal aplicada a la ventana y componentes base de la interfaz."""


def start_button_style() -> str:
    """Retorna la hoja de estilo QSS para el botón de inicio de transmisión ('START').

    Returns:
        Cadena con la propiedad de estilo QSS en tonos verdes.
    """
    return f"background: #0d2b0d; color: {THEME_GREEN}; border-color: {THEME_GREEN}44;"


def stop_button_style() -> str:
    """Retorna la hoja de estilo QSS para el botón de detención de transmisión ('STOP').

    Returns:
        Cadena con la propiedad de estilo QSS en tonos rojos de alerta.
    """
    return f"background: #2b0d0d; color: {THEME_RED}; border-color: {THEME_RED}44;"


def unit_button_style() -> str:
    """Retorna la hoja de estilo QSS para el botón selector de unidades de fuerza (N / kg).

    Returns:
        Cadena con la propiedad de estilo QSS en tonos cyan.
    """
    return f"background: #1a1a3a; color: {THEME_CYAN}; border-color: {THEME_CYAN}44;"


def arm_button_style() -> str:
    """Retorna la hoja de estilo QSS para el botón de armado del sistema de ignición ('ARM').

    Returns:
        Cadena con la propiedad de estilo QSS en tonos ámbar de precaución.
    """
    return "background: #2b1a00; color: #ffaa00; border: 2px solid #ffaa0066; padding: 10px 24px;"


def fire_button_enabled_style() -> str:
    """Retorna la hoja de estilo QSS para el botón de disparo ('FIRE') habilitado.

    Returns:
        Cadena con la propiedad de estilo QSS en rojo brillante de ignición inminente.
    """
    return "background: #4a0000; color: #ff2222; border: 2px solid #ff2222; padding: 10px 24px;"


def fire_button_disabled_style() -> str:
    """Retorna la hoja de estilo QSS para el botón de disparo ('FIRE') deshabilitado en modo seguro.

    Returns:
        Cadena con la propiedad de estilo QSS atenuado en reposo.
    """
    return "background: #1a0000; color: #444444; border: 2px solid #44444444; padding: 10px 24px;"


def connected_status_style() -> str:
    """Retorna la hoja de estilo QSS para la etiqueta de estado cuando el puerto está conectado.

    Returns:
        Cadena de estilo QSS con tipografía verde y en negrita.
    """
    return f"color: {THEME_GREEN}; font-size: 11px; font-weight: bold;"


def disconnected_status_style() -> str:
    """Retorna la hoja de estilo QSS para la etiqueta de estado cuando el puerto está desconectado.

    Returns:
        Cadena de estilo QSS con tipografía roja y en negrita.
    """
    return f"color: {THEME_RED}; font-size: 11px; font-weight: bold;"


def kpi_card_style(accent_color: str = THEME_CYAN) -> str:
    """Retorna la hoja de estilo QSS para tarjetas de métricas numéricas (KpiCard).

    Args:
        accent_color: Código de color hexadecimal para el borde de acento.

    Returns:
        Cadena de estilo QSS con fondo oscuro y borde translúcido según el color provisto.
    """
    return f"background: {THEME_PANEL_BG}; border: 1px solid {accent_color}44; border-radius: 8px;"
