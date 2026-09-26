"""
Widget del panel de ignición.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal

class IgnitionPanel(QWidget):
    """
    Panel de ignición con controles de armado y disparo.
    """
    fire_triggered = pyqtSignal()

    def __init__(self, parent=None) -> None:
        """
        Inicializa el panel de ignición.
        
        Args:
            parent: Widget padre.
        """
        super().__init__(parent)
        self._armed: bool = False
        self._build_ui()

    def _build_ui(self) -> None:
        """Construye la interfaz de ignición."""
        ign_row = QHBoxLayout(self)
        ign_row.setContentsMargins(0, 0, 0, 0)
        
        self.btn_arm = QPushButton("ARM")
        self.btn_arm.setStyleSheet("background:#2b1a00;color:#ffaa00;border:2px solid #ffaa0066;padding:10px 24px;")
        self.btn_arm.clicked.connect(self.toggle_arm)
        
        self.btn_fire = QPushButton("FIRE")
        self.btn_fire.setStyleSheet("background:#1a0000;color:#444444;border:2px solid #44444444;padding:10px 24px;")
        self.btn_fire.setEnabled(False)
        self.btn_fire.clicked.connect(self.fire_triggered.emit)
        
        self.lbl_arm_status = QLabel("SISTEMA: SAFE")
        self.lbl_arm_status.setStyleSheet("color:#ff4444;")
        
        ign_row.addWidget(self.btn_arm)
        ign_row.addWidget(self.btn_fire)
        ign_row.addSpacing(16)
        ign_row.addWidget(self.lbl_arm_status)
        ign_row.addStretch()

    @property
    def is_armed(self) -> bool:
        """
        Devuelve el estado de armado actual.
        
        Returns:
            bool: Verdadero si está armado.
        """
        return self._armed

    def toggle_arm(self) -> None:
        """Alterna el estado de armado."""
        if self._armed:
            self.disarm()
        else:
            self._arm()

    def _arm(self) -> None:
        """Arma el sistema habilitando el disparo."""
        self._armed = True
        self.btn_arm.setStyleSheet("background:#ffaa00;color:#000000;border:2px solid #ffaa00;padding:10px 24px;font-weight:bold;")
        self.btn_fire.setEnabled(True)
        self.btn_fire.setStyleSheet("background:#2b0000;color:#ff4444;border:2px solid #ff4444;padding:10px 24px;font-weight:bold;")
        self.lbl_arm_status.setText("SISTEMA: ARMED")
        self.lbl_arm_status.setStyleSheet("color:#ffaa00;font-weight:bold;")

    def disarm(self) -> None:
        """Desarma el sistema, bloqueando el disparo."""
        self._armed = False
        self.btn_arm.setStyleSheet("background:#2b1a00;color:#ffaa00;border:2px solid #ffaa0066;padding:10px 24px;")
        self.btn_fire.setEnabled(False)
        self.btn_fire.setStyleSheet("background:#1a0000;color:#444444;border:2px solid #44444444;padding:10px 24px;")
        self.lbl_arm_status.setText("SISTEMA: SAFE")
        self.lbl_arm_status.setStyleSheet("color:#ff4444;")
