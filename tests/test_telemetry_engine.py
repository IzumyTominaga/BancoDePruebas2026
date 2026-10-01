import pytest
from core.telemetry_engine import TelemetryEngine

def test_process_reading_returns_correct_type() -> None:
    """Verifica que el procesamiento devuelva la estructura de datos correcta."""
    engine = TelemetryEngine()
    reading = engine.process_reading(15.0, 1, -50)
    assert reading.seq == 1
    assert reading.rssi == -50
    assert reading.thrust_n > 0.0
    assert hasattr(reading, "impulse_ns")

def test_tare_adjusts_offset() -> None:
    """Verifica que la funcionalidad de tara compense valores basales."""
    engine = TelemetryEngine()
    
    # Procesar varias lecturas que sirvan de base para la tara
    for _ in range(10):
        engine.process_reading(5.0, 1, -50)
        
    engine.tare()
    
    # Después de tarar 5.0N, una nueva lectura de 5.0N debería quedar muy cerca de 0
    reading = engine.process_reading(5.0, 2, -50)
    assert reading.thrust_n < 1.0  # El umbral filtraría o el valor real sería cercano a cero

def test_clear_resets_data() -> None:
    """Verifica que los datos temporales se borren al limpiar el motor de telemetría."""
    engine = TelemetryEngine()
    engine.process_reading(20.0, 1, -45)
    assert len(engine.time_series) > 0
    
    engine.clear()
    assert len(engine.time_series) == 0
    assert len(engine.thrust_series) == 0
    assert len(engine.impulse_series) == 0

def test_toggle_unit_switches_properly() -> None:
    """Verifica que cambiar la unidad altere los factores de conversión y bandera."""
    engine = TelemetryEngine()
    estado_inicial = engine.is_kg
    
    engine.toggle_unit()
    assert engine.is_kg != estado_inicial
    
    engine.toggle_unit()
    assert engine.is_kg == estado_inicial

def test_impulse_accumulation() -> None:
    """Verifica la integración (acumulación) del impulso en el tiempo."""
    engine = TelemetryEngine()
    
    # Procesar con valores considerables por encima del threshold
    engine.process_reading(100.0, 1, -50)
    engine.process_reading(100.0, 2, -50)
    
    assert len(engine.impulse_series) == 2
    # El impulso debería ser positivo si dt es positivo y thrust > umbral
    assert engine.impulse_series[-1] >= 0.0

def test_threshold_filtering() -> None:
    """Verifica que las fuerzas menores al umbral configurado se descarten (pasen a 0)."""
    engine = TelemetryEngine()
    # Enviamos un valor que presumiblemente sea menor al THRUST_THRESHOLD habitual
    engine.process_reading(0.01, 1, -40)
    assert engine.thrust_series[-1] == 0.0


def test_median_filter_rejects_an_isolated_spike() -> None:
    engine = TelemetryEngine(thrust_threshold=0.1, filter_window_size=5)

    for seq, value in enumerate([0.0, 0.0, 0.0, 100.0, 0.0], start=1):
        reading = engine.process_reading(value, seq, -40)

    assert reading.thrust_n == 0.0


def test_tare_uses_signed_raw_signal() -> None:
    engine = TelemetryEngine(thrust_threshold=0.1, filter_window_size=1)

    for seq in range(1, 8):
        engine.process_reading(-3.0, seq, -40)
    engine.tare()
    reading = engine.process_reading(-3.0, 8, -40)

    assert reading.thrust_n == 0.0
