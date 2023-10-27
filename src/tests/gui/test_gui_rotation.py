from controllers.main_window_controller import MainWindowController
from PySide6.QtCore import QTimer
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QSignalSpy
from pytestqt.qtbot import QtBot


def test_rotation(
    view: QQuickView, main_window_controller: MainWindowController, qtbot: QtBot
) -> None:
    timer = QTimer()
    timer.start(10)

    spy = QSignalSpy(main_window_controller.valueChanged)

    timer.timeout.connect(main_window_controller.rotate)

    def is_rotated() -> None:
        assert main_window_controller.rotateValue.r >= 50

    qtbot.waitUntil(is_rotated)

    assert spy.count() == 5
    assert main_window_controller.rotateValue.r == 50

    del view
