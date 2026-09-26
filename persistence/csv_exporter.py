"""
Modulo de exportacion de telemetria a formato CSV.

Funciones:
  - export_telemetry_csv: exporta la sesion completa.
  - export_trim_csv: exporta solo el rango recortado con impulso recalculado.
"""

import csv
import logging
import os

from config.constants import GRAVITY

logger = logging.getLogger(__name__)

_HEADERS = ["Tiempo (s)", "Empuje (N)", "Empuje (kg)", "Impulso acum (Ns)", "Impulso acum (kgs)"]


def export_telemetry_csv(
    filepath: str,
    time_data: list[float],
    thrust_data: list[float],
) -> None:
    """
    Exporta los datos de telemetria a un archivo CSV con columnas de tiempo y empuje.

    Args:
        filepath: Ruta completa del archivo destino.
        time_data: Lista de tiempos transcurridos en segundos.
        thrust_data: Lista de empuje medido en Newtons.

    Raises:
        ValueError: Si las listas tienen longitudes diferentes.
        OSError: Si ocurre un error de I/O.
    """
    if len(time_data) != len(thrust_data):
        msg = (
            f"Discrepancia en longitudes: time_data={len(time_data)}, "
            f"thrust_data={len(thrust_data)}"
        )
        logger.error(msg)
        raise ValueError(msg)

    dirname = os.path.dirname(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tiempo (s)", "Empuje (N)", "Empuje (kg)"])
            for t, n in zip(time_data, thrust_data):
                writer.writerow([round(t, 4), round(n, 4), round(n / GRAVITY, 4)])
        logger.info(
            "Telemetria exportada a '%s' (%d filas)", filepath, len(time_data)
        )
    except OSError as e:
        logger.error("Error al exportar CSV a '%s': %s", filepath, e)
        raise


def export_trim_csv(
    filepath: str,
    time_data: list[float],
    thrust_data: list[float],
    t_start: float,
    t_end: float,
) -> int:
    """
    Exporta solo el rango de tiempo [t_start, t_end] con impulso acumulado recalculado.

    Filtra los datos dentro del rango seleccionado y recalcula el impulso acumulado
    desde cero, tal como si el ensayo hubiera comenzado en t_start.

    Args:
        filepath: Ruta del archivo CSV de salida.
        time_data: Lista completa de tiempos en segundos.
        thrust_data: Lista completa de empuje en Newtons.
        t_start: Tiempo de inicio del recorte (inclusive).
        t_end: Tiempo de fin del recorte (inclusive).

    Returns:
        Numero de filas exportadas.

    Raises:
        ValueError: Si las listas tienen longitudes diferentes o el rango es invalido.
        OSError: Si ocurre un error de I/O.
    """
    if len(time_data) != len(thrust_data):
        msg = (
            f"Discrepancia en longitudes: time_data={len(time_data)}, "
            f"thrust_data={len(thrust_data)}"
        )
        logger.error(msg)
        raise ValueError(msg)

    if t_start >= t_end:
        raise ValueError(f"t_start ({t_start:.3f}) debe ser menor que t_end ({t_end:.3f})")

    # Filtrar indices dentro del rango
    indices = [i for i, t in enumerate(time_data) if t_start <= t <= t_end]

    if not indices:
        logger.warning(
            "No hay datos en el rango [%.3f, %.3f]. No se exporto nada.", t_start, t_end
        )
        return 0

    dirname = os.path.dirname(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(_HEADERS)

            # Tiempo relativo al inicio del recorte e impulso desde 0
            t_offset = time_data[indices[0]]
            impulse_accum = 0.0
            prev_t = None

            for i in indices:
                t_rel = time_data[i] - t_offset
                n = thrust_data[i]
                if prev_t is not None:
                    dt = time_data[i] - time_data[i - 1] if i > 0 else 0.0
                    impulse_accum += n * dt
                prev_t = time_data[i]
                writer.writerow([
                    round(t_rel, 4),
                    round(n, 4),
                    round(n / GRAVITY, 4),
                    round(impulse_accum, 4),
                    round(impulse_accum / GRAVITY, 4),
                ])

        rows = len(indices)
        logger.info(
            "Recorte exportado a '%s' (%d filas, rango %.2fs-%.2fs)",
            filepath, rows, t_start, t_end,
        )
        return rows
    except OSError as e:
        logger.error("Error al exportar recorte CSV a '%s': %s", filepath, e)
        raise
