# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import os
import sys
from pathlib import Path

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

from controllers.main_window_console import MainWindowConsole
from controllers.main_window_controller import MainWindowController

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()

    main_window_controller = MainWindowController()
    main_window_console = MainWindowConsole()
    timer = QTimer()
    timer.start(100)
    view.setInitialProperties(
        {
            "mainWindowController": main_window_controller,
            "mainWindowConsole": main_window_console,
        }
    )

    qml_file = os.fspath(Path(__file__).resolve().parent / "views/main.qml")
    view.setSource(QUrl.fromLocalFile(qml_file))
    if view.status() == QQuickView.Status.Error:
        sys.exit(-1)

    timer.timeout.connect(main_window_controller.rotate)

    view.show()
    res = app.exec()
    # Deleting the view before it goes out of scope is required to make sure all child QML instances
    # are destroyed in the correct order.
    del view
    sys.exit(res)
