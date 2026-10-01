"""Motor de procesamiento y cálculo de telemetría para banco de pruebas de motores de cohete.

Este módulo implementa la lógica de cálculo desacoplada de la interfaz gráfica (sin dependencias de PyQt),
incluyendo calibración de tara, filtrado por umbral de ruido, integración temporal de impulso,
detección de pérdida de paquetes y estadísticas globales.
"""

import logging
import time
from collections import deque
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from config.constants import FILTER_WINDOW_SIZE, GRAVITY, THRUST_THRESHOLD
from core.motor_classifier import MotorClassification, clasificar_motor

logger = logging.getLogger(__name__)


@dataclass
class ProcessedReading:
    """Datos procesados de una lectura individual de telemetría.

    Attributes:
        timestamp: Tiempo transcurrido en segundos desde el inicio de la prueba.
        thrust_n: Empuje neto filtrado en Newtons (N).
        thrust_kg: Empuje neto en kilogramos-fuerza (kgf).
        impulse_ns: Impulso total acumulado en Newtons-segundo (N·s).
        impulse_kgs: Impulso total acumulado en kilogramos-segundo (kg·s).
        classification: Clasificación NAR correspondiente al impulso acumulado.
        rssi: Intensidad de señal recibida en dBm (-999 si no aplica).
        seq: Número de secuencia incremental del paquete recibido.
    """

    timestamp: float
    thrust_n: float
    thrust_kg: float
    impulse_ns: float
    impulse_kgs: float
    classification: MotorClassification
    rssi: int
    seq: int


@dataclass
class TelemetryStats:
    """Resumen estadístico del estado acumulado de la telemetría del motor.

    Attributes:
        max_thrust_n: Empuje máximo registrado en Newtons (N).
        max_thrust_kg: Empuje máximo registrado en kilogramos-fuerza (kgf).
        total_impulse_ns: Impulso total acumulado en Newtons-segundo (N·s).
        total_impulse_kgs: Impulso total acumulado en kilogramos-segundo (kg·s).
        classification: Clasificación NAR basada en el impulso total acumulado.
        lost_packets: Cantidad de paquetes de telemetría perdidos detectados por secuencia.
        data_points: Número total de muestras de datos registradas.
    """

    max_thrust_n: float
    max_thrust_kg: float
    total_impulse_ns: float
    total_impulse_kgs: float
    classification: MotorClassification
    lost_packets: int
    data_points: int


class TelemetryEngine:
    """Motor de cálculo y gestión de datos de telemetría para banco de pruebas.

    Encapsula el estado de las series temporales, el cómputo de impulso acumulado,
    la compensación por tara, la conmutación de unidades de visualización y el seguimiento
    de continuidad en los paquetes recibidos.
    """

    def __init__(
        self,
        thrust_threshold: float = THRUST_THRESHOLD,
        filter_window_size: int = FILTER_WINDOW_SIZE,
    ) -> None:
        """Inicializa una nueva instancia del motor de telemetría.

        Args:
            thrust_threshold: Umbral mínimo de empuje en Newtons para filtrar
                ruido basal de la celda de carga. Por defecto THRUST_THRESHOLD.
        """
        if filter_window_size < 1 or filter_window_size % 2 == 0:
            raise ValueError("filter_window_size debe ser un entero impar positivo.")

        self.thrust_threshold: float = thrust_threshold
        self.filter_window_size: int = filter_window_size
        self.time_data: List[float] = []
        self.thrust_n: List[float] = []
        self.impulse_data: List[float] = []
        self.raw_readings: deque[float] = deque(maxlen=filter_window_size)
        self.raw_history: List[float] = []
        self.tare_offset: float = 0.0
        self.start_time: Optional[float] = None
        self.last_seq: int = -1
        self.lost_packets: int = 0
        self.is_kg: bool = False

    def process_reading(self, newtons: float, seq: int, rssi: int) -> ProcessedReading:
        """Procesa una muestra de telemetría cruda y actualiza las series temporales.

        Calcula el tiempo transcurrido desde el inicio, detecta paquetes faltantes a partir
        del número de secuencia, aplica la compensación de tara y el umbral de ruido, e
        integra numéricamente el impulso acumulado.

        Args:
            newtons: Medición de fuerza bruta en Newtons proveniente del sensor.
            seq: Identificador secuencial del paquete de datos.
            rssi: Nivel de potencia de señal recibida en dBm (-999 para conexión alámbrica).

        Returns:
            ProcessedReading: Objeto con los datos procesados, convertidos y clasificados.
        """
        now = time.time()
        if self.start_time is None:
            self.start_time = now
        t = now - self.start_time

        # Monitoreo de pérdidas de paquetes según número de secuencia
        if self.last_seq != -1 and seq > self.last_seq + 1:
            diff = seq - self.last_seq - 1
            self.lost_packets += diff
            logger.warning(
                "Salto de secuencia detectado: %d -> %d (+%d paquetes perdidos)",
                self.last_seq,
                seq,
                diff,
            )
        self.last_seq = seq

        # La tara se conserva en señal firmada. abs() aquí convertiría ruido
        # negativo en empuje positivo y crearía picos artificiales.
        self.raw_readings.append(newtons)
        self.raw_history.append(newtons)
        filtered_newtons = float(np.median(self.raw_readings))
        compensated_newtons = filtered_newtons - self.tare_offset
        thrust_clean = max(0.0, compensated_newtons)
        if thrust_clean < self.thrust_threshold:
            thrust_clean = 0.0

        self.time_data.append(t)
        self.thrust_n.append(thrust_clean)

        # Integración numérica de impulso (N·s)
        if len(self.thrust_n) >= 2:
            dt = self.time_data[-1] - self.time_data[-2]
            if dt < 0.0:
                dt = 0.0
            prev_imp = self.impulse_data[-1] if self.impulse_data else 0.0
            current_impulse_ns = prev_imp + thrust_clean * dt
            self.impulse_data.append(current_impulse_ns)
        else:
            current_impulse_ns = 0.0
            self.impulse_data.append(0.0)

        # Conversiones de unidades físicas y clasificación NAR
        thrust_kg = thrust_clean / GRAVITY
        current_impulse_kgs = current_impulse_ns / GRAVITY
        classification = clasificar_motor(current_impulse_ns)

        return ProcessedReading(
            timestamp=t,
            thrust_n=thrust_clean,
            thrust_kg=thrust_kg,
            impulse_ns=current_impulse_ns,
            impulse_kgs=current_impulse_kgs,
            classification=classification,
            rssi=rssi,
            seq=seq,
        )

    def tare(self) -> None:
        """Establece la tara con la mediana de las últimas 10 lecturas crudas.

        Requiere más de 5 muestras para obtener una referencia robusta al ruido.
        """
        if len(self.raw_history) > 5:
            self.tare_offset = float(np.median(self.raw_history[-10:]))
            self.raw_readings.clear()
            logger.info("Tara establecida en: %.4f N", self.tare_offset)
        else:
            logger.warning("Muestras insuficientes para tara (se requieren más de 5 lecturas).")

    def clear(self) -> None:
        """Reinicia todos los datos acumulados, marcas temporales y contadores de la prueba."""
        self.time_data.clear()
        self.thrust_n.clear()
        self.impulse_data.clear()
        self.raw_readings.clear()
        self.raw_history.clear()
        self.tare_offset = 0.0
        self.start_time = None
        self.last_seq = -1
        self.lost_packets = 0
        logger.info("Datos del motor de telemetría reiniciados.")

    def toggle_unit(self) -> bool:
        """Alterna el estado de visualización entre kilogramos-fuerza y Newtons.

        Returns:
            bool: True si la unidad activa es kilogramos, False si es Newtons.
        """
        self.is_kg = not self.is_kg
        logger.debug("Unidad conmutada: is_kg=%s", self.is_kg)
        return self.is_kg

    def get_trim_stats(self, t_start: float, t_end: float) -> TelemetryStats:
        """Calcula y devuelve las estadisticas consolidadas de un rango de tiempo.

        Args:
            t_start: Tiempo de inicio en segundos.
            t_end: Tiempo de fin en segundos.

        Returns:
            TelemetryStats con los datos exclusivos del rango seleccionado.
        """
        if not self.time_data or t_start >= t_end:
            return TelemetryStats(0.0, 0.0, 0.0, 0.0, clasificar_motor(0.0), 0, 0)

        indices = [i for i, t in enumerate(self.time_data) if t_start <= t <= t_end]
        if not indices:
            return TelemetryStats(0.0, 0.0, 0.0, 0.0, clasificar_motor(0.0), 0, 0)

        trimmed_thrust = [self.thrust_n[i] for i in indices]
        max_thrust_n = max(trimmed_thrust) if trimmed_thrust else 0.0
        max_thrust_kg = max_thrust_n / GRAVITY

        # Calcular impulso numericamente en el rango
        total_impulse_ns = 0.0
        prev_t = None
        for i in indices:
            t = self.time_data[i]
            n = self.thrust_n[i]
            if prev_t is not None:
                dt = t - prev_t
                total_impulse_ns += n * dt
            prev_t = t

        total_impulse_kgs = total_impulse_ns / GRAVITY
        classification = clasificar_motor(total_impulse_ns)

        return TelemetryStats(
            max_thrust_n=max_thrust_n,
            max_thrust_kg=max_thrust_kg,
            total_impulse_ns=total_impulse_ns,
            total_impulse_kgs=total_impulse_kgs,
            classification=classification,
            lost_packets=0,
            data_points=len(indices),
        )

    def get_stats(self) -> TelemetryStats:
        """Calcula y devuelve las estadísticas consolidadas de la sesión actual de telemetría.

        Returns:
            TelemetryStats: Objeto con empuje máximo, impulso total, clasificación NAR,
            paquetes perdidos y número de puntos registrados.
        """
        if self.thrust_n:
            max_thrust_n = max(self.thrust_n)
            max_thrust_kg = max_thrust_n / GRAVITY
            total_impulse_ns = self.impulse_data[-1] if self.impulse_data else 0.0
            total_impulse_kgs = total_impulse_ns / GRAVITY
            classification = clasificar_motor(total_impulse_ns)
        else:
            max_thrust_n = 0.0
            max_thrust_kg = 0.0
            total_impulse_ns = 0.0
            total_impulse_kgs = 0.0
            classification = clasificar_motor(0.0)

        return TelemetryStats(
            max_thrust_n=max_thrust_n,
            max_thrust_kg=max_thrust_kg,
            total_impulse_ns=total_impulse_ns,
            total_impulse_kgs=total_impulse_kgs,
            classification=classification,
            lost_packets=self.lost_packets,
            data_points=len(self.thrust_n),
        )

    @property
    def unit_factor(self) -> float:
        """Factor multiplicativo para convertir Newtons a la unidad activa (1/GRAVITY para kg, 1.0 para N)."""
        return (1.0 / GRAVITY) if self.is_kg else 1.0

    @property
    def time_series(self) -> List[float]:
        """Serie temporal acumulada de lecturas en segundos."""
        return self.time_data

    @property
    def thrust_series(self) -> List[float]:
        """Serie de empuje acumulada en Newtons."""
        return self.thrust_n

    @property
    def impulse_series(self) -> List[float]:
        """Serie de impulso acumulada en Newtons-segundo."""
        return self.impulse_data
