"""
Módulo de guardado automático para la telemetría del banco de pruebas.

Proporciona la clase AutoSaver, un QThread que almacena en disco los datos
de telemetría de forma concurrente y segura mediante una cola thread-safe.
"""

import csv
import logging
import os
import queue
import time

from PyQt6.QtCore import QThread

from config.constants import GRAVITY

logger = logging.getLogger(__name__)


class AutoSaver(QThread):
    """
    Hilo de guardado automático para registrar la telemetría en tiempo real a disco.

    Acumula mediciones en una cola thread-safe (queue.Queue) y las escribe
    periódicamente en un archivo CSV para evitar pérdida de datos ante caídas.
    """

    def __init__(self, filepath: str) -> None:
        """
        Inicializa el guardador automático y escribe la cabecera en el archivo CSV.

        Args:
            filepath: Ruta completa del archivo CSV en el que se guardarán los datos.
        """
        super().__init__()
        self.filepath: str = filepath
        self.queue: queue.Queue[tuple[float, float, float]] = queue.Queue()
        self.running: bool = True
        self._write_header()

    def _write_header(self) -> None:
        """Crea el archivo y escribe el encabezado con las columnas de telemetría."""
        try:
            dirname = os.path.dirname(self.filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    "Tiempo (s)",
                    "Empuje (N)",
                    "Empuje (kg)",
                    "Impulso acum (Ns)",
                    "Impulso acum (kgs)",
                ])
        except OSError as e:
            logger.error("Error al escribir encabezado de autoguardado en '%s': %s", self.filepath, e)

    def add_row(self, t: float, n: float, imp: float) -> None:
        """
        Agrega una nueva fila de telemetría a la cola de guardado.

        Args:
            t: Marca de tiempo transcurrido en segundos.
            n: Empuje medido en Newtons.
            imp: Impulso acumulado en Newton-segundos (Ns).
        """
        self.queue.put((t, n, imp))

    def _flush_queue(self) -> None:
        """Extrae todos los elementos pendientes de la cola y los escribe en el archivo CSV."""
        rows: list[tuple[float, float, float]] = []
        while not self.queue.empty():
            try:
                rows.append(self.queue.get_nowait())
            except queue.Empty:
                break

        if rows:
            try:
                with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    for t, n, imp in rows:
                        w.writerow([
                            round(t, 4),
                            round(n, 4),
                            round(n / GRAVITY, 4),
                            round(imp, 4),
                            round(imp / GRAVITY, 4),
                        ])
                        self.queue.task_done()
            except OSError as e:
                logger.error("Error al escribir filas de autoguardado en '%s': %s", self.filepath, e)

    def run(self) -> None:
        """Bucle de ejecución periódica que vuelca los datos de la cola al archivo CSV."""
        while self.running:
            self._flush_queue()
            time.sleep(0.5)
        # Volcado final al detener el hilo
        self._flush_queue()

    def stop(self) -> None:
        """Detiene el hilo de guardado y espera a que finalice su ejecución."""
        self.running = False
        self.wait()
