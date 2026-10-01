import sys
import logging
from PyQt6.QtWidgets import QApplication
from ui.main_window import RocketDashboard
from ui.intro_splash import IntroSplash

def main() -> None:
    """Punto de entrada principal para la aplicación de telemetría Horus."""
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    app = QApplication(sys.argv)
    window = RocketDashboard()

    splash = IntroSplash()
    splash.finished.connect(window.show)
    splash.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
