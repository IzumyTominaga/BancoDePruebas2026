from ui.dialogs.analysis_window import _percent_change


def test_percent_change_reports_improvement_and_regression():
    assert _percent_change(10.0, 12.0) == "+20.0"
    assert _percent_change(10.0, 8.0) == "-20.0"


def test_percent_change_handles_zero_reference():
    assert _percent_change(0.0, 10.0) == "—"
