import os
import sys
from pathlib import Path

import ingenialogger
from controllers.drive_controller import DriveController
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication

# Needed for styling.
# Created with pyside6-rcc using resources.qrc and qtquickcontrols.conf.
import resources  # noqa: F401

if __name__ == "__main__":
    # Init the logger util.
    ingenialogger.configure_logger(level=ingenialogger.LoggingLevel.INFO)

    # Create the application.
    app = QApplication(sys.argv)

    # Set the favicon.
    app.setWindowIcon(QIcon("assets/novantaMotionFavicon.png"))

    # Insert QML Quick view into the application.
    view = QQuickView()
    qml_file = os.fspath(Path(__file__).resolve().parent / "views/main.qml")
    engine = QQmlApplicationEngine()

    # Init the controller and make it availble to our .qml files.
    drive_controller = DriveController()
    engine.setInitialProperties({"driveController": drive_controller})

    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    # Start the application.
    sys.exit(app.exec())
