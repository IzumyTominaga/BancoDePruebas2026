"""Módulo para la resolución y gestión de rutas de recursos."""

import os
import sys


def resource_path(relative_path: str) -> str:
    """Obtiene la ruta absoluta a un recurso, compatible con PyInstaller y entorno de desarrollo.

    En un ejecutable empaquetado por PyInstaller (modo onefile), los archivos se descomprimen
    en un directorio temporal accesible mediante `sys._MEIPASS`. En modo desarrollo normal,
    se resuelve la ruta relativa respecto al directorio de trabajo actual.

    Args:
        relative_path: Ruta relativa del archivo o recurso (ej. 'HorusSlogan.png').

    Returns:
        Ruta absoluta al recurso como cadena de texto.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
