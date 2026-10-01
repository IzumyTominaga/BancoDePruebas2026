from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QDialog

from ui.widgets.ignition_panel import IgnitionPanel


def test_fire_is_disabled_while_safe() -> None:
    app = QApplication.instance() or QApplication([])
    panel = IgnitionPanel()

    assert not panel.is_armed
    assert not panel.btn_fire.isEnabled()


def test_arm_enables_fire_and_disarm_disables_it() -> None:
    app = QApplication.instance() or QApplication([])
    panel = IgnitionPanel()

    panel.toggle_arm()
    assert panel.is_armed
    assert panel.btn_fire.isEnabled()

    panel.disarm()
    assert not panel.is_armed
    assert not panel.btn_fire.isEnabled()


def test_fire_request_disarms_after_cancel(monkeypatch) -> None:
    app = QApplication.instance() or QApplication([])
    panel = IgnitionPanel()
    panel.toggle_arm()

    monkeypatch.setattr(
        "ui.widgets.ignition_panel.FireCodeDialog.exec",
        lambda dialog: QDialog.DialogCode.Rejected,
    )
    panel._request_fire()

    assert not panel.is_armed
    assert not panel.btn_fire.isEnabled()
