"""Módulo para la gestión y persistencia de configuración del usuario."""

import json
import logging
import os
from typing import Any, Dict, Optional

from config.constants import CONFIG_FILE

logger = logging.getLogger(__name__)


class AppSettings:
    """Gestiona la persistencia de configuraciones de la aplicación en formato JSON.

    Permite almacenar y recuperar parámetros entre sesiones, tales como el último puerto
    serie seleccionado, modos preferidos o calibraciones previas.
    """

    def __init__(self, config_file: Optional[str] = None) -> None:
        """Inicializa el gestor de configuración.

        Args:
            config_file: Ruta opcional del archivo JSON. Si no se provee,
                se utiliza la ruta por defecto en el directorio home del usuario.
        """
        self.config_file: str = config_file or CONFIG_FILE
        self._data: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """Carga los parámetros desde el archivo JSON de configuración.

        Si el archivo no existe o contiene un formato inválido, inicializa un diccionario
        vacío y registra el suceso mediante logging.

        Returns:
            Diccionario con las opciones de configuración recuperadas.
        """
        if not os.path.exists(self.config_file):
            logger.info("Archivo de configuración no encontrado en '%s'. Usando valores predeterminados.", self.config_file)
            self._data = {}
            return self._data

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self._data = json.load(f)
            logger.info("Configuración cargada correctamente desde '%s'.", self.config_file)
        except json.JSONDecodeError as e:
            logger.warning("El archivo de configuración en '%s' está corrupto o mal formado: %s", self.config_file, e)
            self._data = {}
        except OSError as e:
            logger.error("Error de E/S al leer la configuración desde '%s': %s", self.config_file, e)
            self._data = {}

        return self._data

    def save(self) -> bool:
        """Guarda la configuración actual en el archivo JSON.

        Crea los directorios necesarios si no existieran previamente.

        Returns:
            True si la operación fue exitosa, False en caso de error.
        """
        try:
            parent_dir = os.path.dirname(self.config_file)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            logger.info("Configuración guardada correctamente en '%s'.", self.config_file)
            return True
        except OSError as e:
            logger.error("No se pudo guardar la configuración en '%s': %s", self.config_file, e)
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene el valor asociado a una clave de configuración.

        Args:
            key: Identificador de la opción deseada.
            default: Valor retornado si la clave no existe.

        Returns:
            El valor almacenado o el valor por defecto provisto.
        """
        return self._data.get(key, default)

    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        """Establece el valor de una clave de configuración.

        Args:
            key: Identificador de la opción.
            value: Valor a asignar.
            auto_save: Si es True, guarda los cambios inmediatamente en disco.
        """
        self._data[key] = value
        logger.debug("Opción de configuración actualizada: '%s' = %s", key, value)
        if auto_save:
            self.save()


def cargar_config(filepath: Optional[str] = None) -> Dict[str, Any]:
    """Carga y retorna la configuración de usuario (función de conveniencia).

    Args:
        filepath: Ruta opcional del archivo JSON.

    Returns:
        Diccionario con los datos de configuración.
    """
    settings = AppSettings(filepath)
    return settings._data


def guardar_config(data: Dict[str, Any], filepath: Optional[str] = None) -> bool:
    """Guarda un diccionario de configuración en disco (función de conveniencia).

    Args:
        data: Diccionario con los datos a persistir.
        filepath: Ruta opcional del archivo JSON.

    Returns:
        True si se guardó exitosamente, False en caso contrario.
    """
    settings = AppSettings(filepath)
    settings._data = data
    return settings.save()
