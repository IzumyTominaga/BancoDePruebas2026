import pytest
from core.motor_classifier import clasificar_motor, MotorClassification

def test_clasificar_motor_zero() -> None:
    """Prueba la clasificación con un impulso nulo (0 Ns)."""
    resultado = clasificar_motor(0.0)
    assert hasattr(resultado, 'letter')
    assert hasattr(resultado, 'percentage')
    
def test_clasificar_motor_negative() -> None:
    """Prueba la clasificación con impulso negativo."""
    resultado = clasificar_motor(-5.0)
    assert isinstance(resultado.letter, str)
    assert resultado.percentage >= 0.0

def test_clasificar_motor_clase_a() -> None:
    """Prueba que el límite medio de Clase A (aprox. 1.88 Ns) se identifique correctamente."""
    # Límites Clase A: 1.26 - 2.50 Ns
    resultado = clasificar_motor(2.0)
    assert resultado.letter == "A"
    assert 0 <= resultado.percentage <= 100

def test_clasificar_motor_clase_g() -> None:
    """Prueba que el límite medio de Clase G (aprox. 120 Ns) se identifique correctamente."""
    # Límites Clase G: 80.01 - 160.00 Ns
    resultado = clasificar_motor(120.0)
    assert resultado.letter == "G"

def test_clasificar_motor_clase_m() -> None:
    """Prueba que el límite medio de Clase M se identifique correctamente."""
    # Límites Clase M: 5120.01 - 10240.00 Ns
    resultado = clasificar_motor(7000.0)
    assert resultado.letter == "M"

def test_clasificar_motor_grande() -> None:
    """Prueba el comportamiento con un impulso excesivamente grande."""
    resultado = clasificar_motor(999999.0)
    assert isinstance(resultado.letter, str)
