"""
Módulo de protocolos y modos de comunicación para el banco de pruebas.

Define los modos de conexión (cable y LoRa), las configuraciones de paquetes binarios
asociados y las constantes de protocolo.
"""

from dataclasses import dataclass
from enum import Enum

RSSI_NOT_AVAILABLE: int = -999
"""Valor indicador de que el RSSI no está disponible (ej. en modo cable)."""


class ConnectionMode(str, Enum):
    """Modos de conexión disponibles para la telemetría del banco de pruebas."""

    CABLE = "cable"
    LORA = "lora"


@dataclass(frozen=True)
class ProtocolConfig:
    """Configuración de deserialización de paquetes binarios de telemetría."""

    packet_size: int
    struct_format: str
    has_rssi: bool


PROTOCOL_CONFIGS: dict[ConnectionMode, ProtocolConfig] = {
    ConnectionMode.CABLE: ProtocolConfig(
        packet_size=8,
        struct_format="<fI",
        has_rssi=False,
    ),
    ConnectionMode.LORA: ProtocolConfig(
        packet_size=9,
        struct_format="<fIb",
        has_rssi=True,
    ),
}
