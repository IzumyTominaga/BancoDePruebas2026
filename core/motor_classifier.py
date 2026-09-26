"""Módulo de clasificación de motores de cohete según estándares NAR.

Proporciona la lógica y estructuras de datos para categorizar motores de cohete
en base a su impulso total en Newtons-segundo (N·s), de acuerdo con la escala
de la National Association of Rocketry (NAR).
"""

from dataclasses import dataclass
from typing import Optional

from config.nar_classes import NAR_CLASSES


@dataclass
class MotorClassification:
    """Representa la clasificación NAR de un motor de cohete.

    Attributes:
        letter: Letra de la clase NAR asignada ('A' a 'V', 'V+' si excede la clase máxima, o '—' si no alcanza el mínimo).
        percentage: Porcentaje relativo alcanzado dentro del rango de la clase actual (0.0% a 100.0%).
    """

    letter: str
    percentage: float


def clasificar_motor(impulso_ns: float) -> MotorClassification:
    """Clasifica un motor de cohete según el estándar NAR a partir de su impulso total.

    Evalúa el impulso total acumulado en Newtons-segundo contra los intervalos definidos
    en NAR_CLASSES. Calcula el porcentaje relativo del avance dentro de la categoría encontrada.

    Args:
        impulso_ns: Impulso total calculado en Newtons-segundo (N·s).

    Returns:
        MotorClassification: Objeto con la letra de la clase y el porcentaje de completitud.
            Retorna ('—', 0.0) si el impulso es inferior a la clase 'A' (< 1.26 N·s),
            o ('V+', 100.0) si es igual o superior a 5,242,880 N·s.
    """
    for letra, lo, hi in NAR_CLASSES:
        if lo <= impulso_ns < hi:
            porcentaje = (impulso_ns - lo) / (hi - lo) * 100.0
            return MotorClassification(letter=letra, percentage=porcentaje)

    if impulso_ns >= 5242880.0:
        return MotorClassification(letter="V+", percentage=100.0)

    return MotorClassification(letter="—", percentage=0.0)
