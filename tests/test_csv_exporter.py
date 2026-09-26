import os, csv
from persistence.csv_exporter import export_telemetry_csv

def test_export_telemetry_csv(tmp_path):
    filepath = os.path.join(tmp_path, 'telemetry_test.csv')
    time_data = [0.0, 0.5, 1.0]
    thrust_data = [0.0, 25.0, 0.0]
    export_telemetry_csv(filepath, time_data, thrust_data)
    assert os.path.exists(filepath)
    with open(filepath, 'r', newline='') as f:
        rows = list(csv.reader(f))
    assert len(rows) == 4
    assert rows[0] == ['Tiempo (s)', 'Empuje (N)', 'Empuje (kg)']
    assert float(rows[1][0]) == 0.0
    assert float(rows[2][1]) == 25.0

def test_export_telemetry_csv_empty(tmp_path):
    filepath = os.path.join(tmp_path, 'telemetry_empty.csv')
    export_telemetry_csv(filepath, [], [])
    assert os.path.exists(filepath)
    with open(filepath, 'r', newline='') as f:
        rows = list(csv.reader(f))
    assert len(rows) == 1
    assert rows[0] == ['Tiempo (s)', 'Empuje (N)', 'Empuje (kg)']
