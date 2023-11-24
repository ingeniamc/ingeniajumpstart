import os
import sys
from pathlib import Path

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickView

from src.controllers.main_window_console import MainWindowConsole
from src.controllers.main_window_controller import MainWindowController


@pytest.fixture
def main_window_controller() -> MainWindowController:
    return MainWindowController()


@pytest.fixture
def main_window_console() -> MainWindowConsole:
    return MainWindowConsole()


@pytest.fixture
def view(
    main_window_controller: MainWindowController, main_window_console: MainWindowConsole
) -> QQuickView:
    view = QQuickView()
    view.setInitialProperties(
        {
            "mainWindowController": main_window_controller,
            "mainWindowConsole": main_window_console,
        }
    )
    qml_file = os.fspath(Path(__file__).resolve().parent.parent / "src/views/main.qml")
    view.setSource(QUrl.fromLocalFile(qml_file))
    if view.status() == QQuickView.Status.Error:
        sys.exit(-1)
    return view
