"""
Barra de herramientas del modo de recorte de grafica.

Aparece debajo de la grafica cuando el usuario activa el modo recorte,
mostrando el rango seleccionado y botones para exportar o cancelar.
"""

import logging
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal

logger = logging.getLogger(__name__)


class TrimToolbar(QWidget):
    """
    Toolbar que se muestra durante el modo de recorte de grafica.

    Muestra el rango de tiempo seleccionado en tiempo real y proporciona
    acciones para exportar el recorte o cancelar la operacion.
    """

    export_trim_requested = pyqtSignal()
    cancel_trim_requested = pyqtSignal()

    def __init__(self, parent=None) -> None:
        """
        Inicializa la toolbar de recorte (inicialmente oculta).

        Args:
            parent: Widget padre opcional.
        """
        super().__init__(parent)
        self._build_ui()
        self.hide()

    def _build_ui(self) -> None:
        """Construye los elementos visuales de la toolbar."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        lbl_mode = QLabel("✂  MODO RECORTE")
        lbl_mode.setStyleSheet(
            "color:#ffaa00;font-size:10px;font-weight:bold;letter-spacing:2px;"
        )

        self.lbl_range = QLabel("Selecciona un rango arrastrando las lineas en la grafica...")
        self.lbl_range.setStyleSheet(
            "color:#00e5ff;font-size:11px;"
            "background:#111133;padding:4px 10px;border-radius:4px;"
        )

        self.btn_export = QPushButton("💾  Exportar recorte")
        self.btn_export.setStyleSheet(
            "background:#0d2b0d;color:#00ff88;"
            "border-color:#00ff8844;padding:6px 14px;"
        )
        self.btn_export.clicked.connect(self.export_trim_requested.emit)

        self.btn_cancel = QPushButton("✕  Cancelar recorte")
        self.btn_cancel.setStyleSheet(
            "background:#2b0d0d;color:#ff4444;"
            "border-color:#ff444444;padding:6px 14px;"
        )
        self.btn_cancel.clicked.connect(self.cancel_trim_requested.emit)

        layout.addWidget(lbl_mode)
        layout.addWidget(self.lbl_range, 1)
        layout.addWidget(self.btn_export)
        layout.addWidget(self.btn_cancel)

    def update_range(self, t_start: float, t_end: float) -> None:
        """
        Actualiza el label con el rango de tiempo seleccionado.

        Args:
            t_start: Tiempo de inicio del recorte en segundos.
            t_end: Tiempo de fin del recorte en segundos.
        """
        duration = max(0.0, t_end - t_start)
        self.lbl_range.setText(
            f"Recorte:  {t_start:.2f}s  →  {t_end:.2f}s  "
            f"({duration:.2f}s de duracion)"
        )
