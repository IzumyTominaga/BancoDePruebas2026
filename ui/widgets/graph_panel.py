"""
Widget de paneles de graficos con soporte de modo recorte.
"""
import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg

logger = logging.getLogger(__name__)


class GraphPanel(QWidget):
    """
    Panel de visualizacion de graficos de empuje e impulso en tiempo real.
    Incluye soporte para modo recorte mediante LinearRegionItem de pyqtgraph.
    """

    trim_range_changed = pyqtSignal(float, float)

    def __init__(self, parent=None) -> None:
        """Inicializa los graficos."""
        super().__init__(parent)
        self._trim_region: pg.LinearRegionItem | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Construye los graficos usando pyqtgraph."""
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        gr = QHBoxLayout()
        gr.setContentsMargins(0, 0, 0, 0)

        self.graph_thrust = pg.PlotWidget()
        self.graph_impulse = pg.PlotWidget()

        self._style_graph(self.graph_thrust, "Tiempo (s)", "Empuje (N)", "#00e5ff")
        self._style_graph(self.graph_impulse, "Tiempo (s)", "Impulso (N\u00b7s)", "#00ff88")

        self.curve_thrust = self.graph_thrust.plot(pen=pg.mkPen("#00e5ff", width=2))
        self.curve_impulse = self.graph_impulse.plot(pen=pg.mkPen("#00ff88", width=2))

        gr.addWidget(self.graph_thrust, 3)
        gr.addWidget(self.graph_impulse, 2)
        outer.addLayout(gr)

    def _style_graph(self, gw: pg.PlotWidget, xlabel: str, ylabel: str, color: str) -> None:
        """Aplica estilo visual al widget del grafico."""
        gw.setBackground("#0d0d1a")
        gw.showGrid(x=True, y=True, alpha=0.15)
        gw.setLabel("left", ylabel, color=color)
        gw.setLabel("bottom", xlabel, color="#445566")

    def update_thrust(self, time_data: list[float], thrust_data: list[float]) -> None:
        """Actualiza el grafico de empuje con nuevos datos."""
        self.curve_thrust.setData(time_data, thrust_data)

    def set_y_labels(self, is_kg: bool) -> None:
        """Actualiza las etiquetas del eje Y segun la unidad seleccionada."""
        if is_kg:
            self.graph_thrust.setLabel("left", "Empuje (kg)", color="#00e5ff")
            self.graph_impulse.setLabel("left", "Impulso (kg·s)", color="#00ff88")
        else:
            self.graph_thrust.setLabel("left", "Empuje (N)", color="#00e5ff")
            self.graph_impulse.setLabel("left", "Impulso (N·s)", color="#00ff88")

    def update_impulse(self, time_data: list[float], impulse_data: list[float]) -> None:
        """Actualiza el grafico de impulso con nuevos datos."""
        self.curve_impulse.setData(time_data, impulse_data)

    def clear(self) -> None:
        """Limpia ambos graficos."""
        self.curve_thrust.setData([], [])
        self.curve_impulse.setData([], [])

    # ── Trim mode ──────────────────────────────────────────────────────────────

    def enable_trim_mode(self, t_min: float = 0.0, t_max: float = 10.0) -> None:
        """
        Activa el modo recorte mostrando un LinearRegionItem arrastrable sobre la grafica.

        El region emitira trim_range_changed cada vez que el usuario mueva las lineas.

        Args:
            t_min: Limite izquierdo inicial de la region de recorte.
            t_max: Limite derecho inicial de la region de recorte.
        """
        if self._trim_region is not None:
            return  # ya activo

        # Calcular posicion inicial: 25%-75% del rango visible
        span = t_max - t_min if t_max > t_min else 10.0
        r0 = t_min + span * 0.25
        r1 = t_min + span * 0.75

        self._trim_region = pg.LinearRegionItem(
            values=[r0, r1],
            brush=pg.mkBrush(0, 255, 136, 30),
            pen=pg.mkPen("#00ff88", width=1, style=pg.QtCore.Qt.PenStyle.DashLine),
            movable=True,
        )
        self._trim_region.sigRegionChanged.connect(self._on_region_changed)
        self.graph_thrust.addItem(self._trim_region)

        # Emitir estado inicial
        self.trim_range_changed.emit(r0, r1)
        logger.info("Modo recorte activado: [%.2f, %.2f]", r0, r1)

    def disable_trim_mode(self) -> None:
        """Desactiva el modo recorte y elimina el LinearRegionItem."""
        if self._trim_region is not None:
            self.graph_thrust.removeItem(self._trim_region)
            self._trim_region = None
            logger.info("Modo recorte desactivado.")

    def get_trim_range(self) -> tuple[float, float]:
        """
        Retorna el rango de tiempo actualmente seleccionado.

        Returns:
            Tupla (t_start, t_end) en segundos. Si no hay region activa, retorna (0, 0).
        """
        if self._trim_region is None:
            return (0.0, 0.0)
        region = self._trim_region.getRegion()
        return (float(region[0]), float(region[1]))

    def _on_region_changed(self) -> None:
        """Slot interno: emite trim_range_changed cuando el usuario mueve la region."""
        if self._trim_region is not None:
            t0, t1 = self._trim_region.getRegion()
            self.trim_range_changed.emit(float(t0), float(t1))
