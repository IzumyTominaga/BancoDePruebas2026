"""Clasificación de motores de cohetería según el estándar de la NAR.

Referencia: Estándar de Clasificación de Motores de la National Association of Rocketry (NAR).
El estándar agrupa los motores alfabéticamente en función del impulso total en Newton-segundos (N·s),
donde cada letra consecutiva duplica la capacidad máxima de impulso de la letra anterior.
"""

from typing import List, Tuple

# Definición de tipo para cada registro de clase: (Letra, Límite inferior N·s, Límite superior N·s)
NarClassEntry = Tuple[str, float, float]

NAR_CLASSES: List[NarClassEntry] = [
    ("A", 1.26, 2.5),
    ("B", 2.5, 5.0),
    ("C", 5.0, 10.0),
    ("D", 10.0, 20.0),
    ("E", 20.0, 40.0),
    ("F", 40.0, 80.0),
    ("G", 80.0, 160.0),
    ("H", 160.0, 320.0),
    ("I", 320.0, 640.0),
    ("J", 640.0, 1280.0),
    ("K", 1280.0, 2560.0),
    ("L", 2560.0, 5120.0),
    ("M", 5120.0, 10240.0),
    ("N", 10240.0, 20480.0),
    ("O", 20480.0, 40960.0),
    ("P", 40960.0, 81920.0),
    ("Q", 81920.0, 163840.0),
    ("R", 163840.0, 327680.0),
    ("S", 327680.0, 655360.0),
    ("T", 655360.0, 1310720.0),
    ("U", 1310720.0, 2621440.0),
    ("V", 2621440.0, 5242880.0),
]


def clasificar_motor(impulso_ns: float) -> Tuple[str, float]:
    """Clasifica un motor de cohete a partir de su impulso total acumulado.

    Recorre la tabla de clases NAR para encontrar la categoría correspondiente
    y calcula el porcentaje porcentual completado dentro de dicho intervalo.

    Args:
        impulso_ns: Impulso total calculado en Newton-segundos (N·s).

    Returns:
        Tupla con:
            - Letra de la clase ('A' a 'V', 'V+' si supera la clase máxima, o '—' si es inferior a 'A').
            - Porcentaje alcanzado dentro del rango de dicha clase (0.0 a 100.0).
    """
    for letra, lo, hi in NAR_CLASSES:
        if lo <= impulso_ns < hi:
            porcentaje = (impulso_ns - lo) / (hi - lo) * 100.0
            return letra, porcentaje

    if impulso_ns >= 5242880.0:
        return "V+", 100.0

    return "—", 0.0
