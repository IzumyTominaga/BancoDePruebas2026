import csv

import pytest

from persistence.csv_loader import load_telemetry_csv


def test_loads_exported_csv_and_calculates_impulse(tmp_path):
    filepath = tmp_path / "telemetria.csv"
    with filepath.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Tiempo (s)", "Empuje (N)", "Empuje (kg)"])
        writer.writerows([[0.0, 0.0, 0.0], [0.5, 10.0, 1.0], [1.0, 20.0, 2.0]])

    data = load_telemetry_csv(str(filepath))

    assert data.time_data == [0.0, 0.5, 1.0]
    assert data.thrust_n == [0.0, 10.0, 20.0]
    assert data.impulse_ns == [0.0, 5.0, 15.0]


def test_loads_autosave_csv_with_its_impulse(tmp_path):
    filepath = tmp_path / "autoguardado.csv"
    with filepath.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Tiempo (s)", "Empuje (N)", "Impulso acum (Ns)"])
        writer.writerows([[0.0, 0.0, 0.0], [1.0, 8.0, 8.0]])

    data = load_telemetry_csv(str(filepath))

    assert data.impulse_ns == [0.0, 8.0]


def test_rejects_csv_without_required_columns(tmp_path):
    filepath = tmp_path / "invalido.csv"
    filepath.write_text("otra columna\n1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Tiempo"):
        load_telemetry_csv(str(filepath))
