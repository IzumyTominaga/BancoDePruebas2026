"""
Módulo de lectura de puerto serie para la telemetría del banco de pruebas.

Proporciona la clase SerialReader que procesa de manera asíncrona mediante un QThread
los paquetes binarios entrantes según el protocolo de conexión seleccionado.
"""

import logging
import struct
from typing import Optional

from PyQt6.QtCore import QThread, pyqtSignal
import serial

from communication.protocols import (
    PROTOCOL_CONFIGS,
    RSSI_NOT_AVAILABLE,
    ConnectionMode,
    ProtocolConfig,
)

logger = logging.getLogger(__name__)


class SerialReader(QThread):
    """
    Hilo de lectura asíncrona para comunicación serie con el banco de pruebas.

    Lee los paquetes binarios enviados por el microcontrolador (por cable o LoRa),
    los deserializa según la configuración del protocolo y emite señales con los datos
    recibidos o cuando se produce una desconexión.
    """

    data_received = pyqtSignal(float, int, int)
    disconnected = pyqtSignal()

    def __init__(
        self,
        port: str,
        baudrate: int,
        mode: ConnectionMode | str = ConnectionMode.CABLE,
    ) -> None:
        """
        Inicializa el lector serie con el puerto, velocidad y modo especificados.

        Args:
            port: Identificador del puerto serie (ej. 'COM3' o '/dev/ttyUSB0').
            baudrate: Velocidad de transmisión en baudios (ej. 115200).
            mode: Modo de conexión (ConnectionMode o cadena 'cable'/'lora').
        """
        super().__init__()
        self.port: str = port
        self.baudrate: int = baudrate
        self.mode: ConnectionMode = (
            mode if isinstance(mode, ConnectionMode) else ConnectionMode(mode)
        )
        self.protocol_config: ProtocolConfig = PROTOCOL_CONFIGS[self.mode]
        self.running: bool = False
        self.ser: Optional[serial.Serial] = None

    def run(self) -> None:
        """
        Ejecuta el bucle principal de lectura y decodificación de paquetes del puerto serie.

        Se conecta al puerto, lee datos binarios en bloques según el tamaño definido en
        ProtocolConfig, valida los rangos de empuje y secuencia, y emite la señal
        data_received. Al finalizar o ante un error, emite la señal disconnected.
        """
        pkt_size: int = self.protocol_config.packet_size
        struct_format: str = self.protocol_config.struct_format
        has_rssi: bool = self.protocol_config.has_rssi

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
            self.running = True
            logger.info(
                "Conexión serie establecida en %s a %d baudios (modo: %s)",
                self.port,
                self.baudrate,
                self.mode.value,
            )
            buf = bytearray()
            while self.running:
                try:
                    waiting = self.ser.in_waiting if self.ser.is_open else 0
                    chunk = self.ser.read(waiting or 1)
                except (serial.SerialException, OSError) as e:
                    logger.error("Error al leer del puerto serie %s: %s", self.port, e)
                    break

                if chunk:
                    buf.extend(chunk)

                while len(buf) >= pkt_size:
                    raw = buf[:pkt_size]
                    buf = buf[pkt_size:]
                    try:
                        if has_rssi:
                            newtons, seq, rssi = struct.unpack(struct_format, raw)
                        else:
                            newtons, seq = struct.unpack(struct_format, raw)
                            rssi = RSSI_NOT_AVAILABLE

                        if -500.0 < newtons < 5000.0 and seq < 1_000_000:
                            self.data_received.emit(float(newtons), int(seq), int(rssi))
                        else:
                            logger.warning(
                                "Paquete descartado por valores fuera de rango: N=%.2f, seq=%d",
                                newtons,
                                seq,
                            )
                    except struct.error as e:
                        logger.warning("Error al deserializar paquete binario: %s", e)
        except serial.SerialException as e:
            logger.error("Error al abrir puerto serie %s: %s", self.port, e)
        except Exception as e:
            logger.exception("Error inesperado en SerialReader: %s", e)
        finally:
            self.running = False
            if self.ser and self.ser.is_open:
                try:
                    self.ser.close()
                except Exception as e:
                    logger.debug("Error al cerrar puerto serie en finalización: %s", e)
            self.disconnected.emit()
            logger.info("Puerto serie %s desconectado.", self.port)

    def send_command(self, char: str) -> None:
        """
        Envía un comando de texto o caracter al microcontrolador a través del puerto serie.

        Args:
            char: Carácter o comando a transmitir.
        """
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(char.encode())
                logger.debug("Comando enviado: %s", char)
            except (serial.SerialException, OSError) as e:
                logger.error("Error al enviar comando '%s': %s", char, e)
        else:
            logger.warning("No se pudo enviar comando '%s': puerto serie no abierto", char)

    def stop(self) -> None:
        """Detiene el hilo de lectura y cierra la conexión del puerto serie."""
        self.running = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except (serial.SerialException, OSError) as e:
                logger.error("Error al cerrar el puerto serie durante stop(): %s", e)
        self.wait()
