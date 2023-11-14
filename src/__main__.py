import os
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView

from src.controllers.main_window_console import MainWindowConsole
from src.controllers.main_window_controller import MainWindowController

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    qml_file = os.fspath(Path(__file__).resolve().parent / "views/main.qml")
    engine = QQmlApplicationEngine()

    main_window_controller = MainWindowController()
    main_window_console = MainWindowConsole()

    engine.setInitialProperties(
        {
            "mainWindowController": main_window_controller,
            "mainWindowConsole": main_window_console,
        }
    )
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
