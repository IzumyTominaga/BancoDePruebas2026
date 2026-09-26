"""
Dialogo de confirmacion inteligente para exportacion de CSV.

Aparece cuando el usuario intenta exportar manualmente y ya existe
un archivo CSV autoguardado activo en la sesion.
"""

import logging
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt

from persistence.csv_exporter import export_telemetry_csv

logger = logging.getLogger(__name__)

_STYLE = (
    "QDialog{background:#0d0d1a;}"
    "QLabel{color:#cccccc;font-family:'Courier New',monospace;}"
    "QPushButton{background:#1e1e2e;color:#dddddd;border-radius:4px;"
    "padding:8px 16px;font-weight:bold;"
    "font-family:'Courier New',monospace;border:1px solid #333355;}"
    "QPushButton:hover{background:#2a2a3e;border-color:#5555aa;}"
    "QPushButton:pressed{background:#111122;}"
)


class ExportConfirmDialog(QDialog):
    """
    Dialogo de confirmacion para exportar datos cuando ya existe un CSV autoguardado.

    Presenta tres opciones al usuario:
      - Guardar con nuevo nombre (abre QFileDialog)
      - Reescribir el archivo autoguardado existente
      - Cancelar sin hacer cambios
    """

    def __init__(
        self,
        autosave_filepath: str,
        time_data: list[float],
        thrust_data: list[float],
        parent=None,
    ) -> None:
        """
        Inicializa el dialogo.

        Args:
            autosave_filepath: Ruta del CSV autoguardado actualmente activo.
            time_data: Serie temporal en segundos.
            thrust_data: Serie de empuje en Newtons.
            parent: Widget padre opcional.
        """
        super().__init__(parent)
        self._autosave_filepath = autosave_filepath
        self._time_data = time_data
        self._thrust_data = thrust_data
        self._result_path: str | None = None

        self.setWindowTitle("Exportar CSV")
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setStyleSheet(_STYLE)
        self._build_ui()

    def _build_ui(self) -> None:
        """Construye los elementos visuales del dialogo."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl_title = QLabel("⚠  Ya existe un CSV autoguardado")
        lbl_title.setStyleSheet("color:#ffaa00;font-size:14px;font-weight:bold;")
        layout.addWidget(lbl_title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color:#222244;")
        layout.addWidget(sep)

        lbl_info = QLabel("Archivo autoguardado activo:")
        lbl_info.setStyleSheet("color:#888899;font-size:10px;")
        layout.addWidget(lbl_info)

        lbl_path = QLabel(self._autosave_filepath)
        lbl_path.setStyleSheet(
            "color:#00e5ff;font-size:10px;"
            "background:#111133;padding:6px;border-radius:4px;"
        )
        lbl_path.setWordWrap(True)
        lbl_path.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(lbl_path)

        lbl_q = QLabel("¿Este CSV ya fue guardado. Estas seguro que quieres reescribirlo?")
        lbl_q.setStyleSheet("color:#cccccc;margin-top:6px;")
        layout.addWidget(lbl_q)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_new = QPushButton("✔  Guardar con nuevo nombre")
        self.btn_new.setStyleSheet(
            "background:#0d2b0d;color:#00ff88;border-color:#00ff8844;"
        )
        self.btn_new.clicked.connect(self._save_new_name)

        self.btn_overwrite = QPushButton("Si, Reescribir")
        self.btn_overwrite.setStyleSheet(
            "background:#2b1a00;color:#ffaa00;border-color:#ffaa0044;"
        )
        self.btn_overwrite.clicked.connect(self._overwrite)

        self.btn_cancel = QPushButton("No, Cancelar")
        self.btn_cancel.setStyleSheet(
            "background:#2b0d0d;color:#ff4444;border-color:#ff444444;"
        )
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_overwrite)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def _save_new_name(self) -> None:
        """Abre un QFileDialog para elegir una nueva ruta y exporta los datos."""
        suggested = Path(self._autosave_filepath).stem + "_exportado.csv"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar CSV con nuevo nombre",
            str(Path(self._autosave_filepath).parent / suggested),
            "CSV (*.csv)",
        )
        if path:
            try:
                export_telemetry_csv(path, self._time_data, self._thrust_data)
                self._result_path = path
                logger.info("CSV exportado con nuevo nombre: %s", path)
                self.accept()
            except Exception as exc:
                logger.error("Error exportando CSV: %s", exc)

    def _overwrite(self) -> None:
        """Reescribe el archivo autoguardado con los datos actuales de la sesion."""
        try:
            export_telemetry_csv(
                self._autosave_filepath, self._time_data, self._thrust_data
            )
            self._result_path = self._autosave_filepath
            logger.info("CSV autoguardado reescrito: %s", self._autosave_filepath)
            self.accept()
        except Exception as exc:
            logger.error("Error reescribiendo CSV autoguardado: %s", exc)

    @property
    def result_path(self) -> str | None:
        """Ruta del archivo exportado, o None si se cancelo."""
        return self._result_path
