import os
import sys
from pathlib import Path

import ingenialogger
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication

import resources  # noqa: F401
from src.controllers.drive_controller import DriveController

if __name__ == "__main__":
    ingenialogger.configure_logger(level=ingenialogger.LoggingLevel.INFO)
    app = QApplication(sys.argv)
    app.setWindowIcon(
        QIcon(
            os.fspath(
                Path(__file__).resolve().parent / "assets/novantaMotionFavicon.png"
            )
        )
    )

    view = QQuickView()
    qml_file = os.fspath(Path(__file__).resolve().parent / "views/main.qml")
    engine = QQmlApplicationEngine()

    drive_controller = DriveController()

    engine.setInitialProperties({"driveController": drive_controller})
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    ret = app.exec()
    drive_controller.mcs.stop_motion_controller_thread()
    sys.exit(ret)
