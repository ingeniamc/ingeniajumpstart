from controllers.main_window_controller import MainWindowController
from PySide6.QtCore import QTimer
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QSignalSpy
from pytestqt.qtbot import QtBot


def test_rotation(
    qtbot: QtBot,
    view: QQuickView,
    main_window_controller: MainWindowController,
) -> None:
    timer = QTimer()
    timer.start(10)

    spy = QSignalSpy(main_window_controller.valueChanged)

    timer.timeout.connect(main_window_controller.rotate)

    qtbot.wait_signal(main_window_controller.valueChanged)

    def is_rotated() -> None:
        assert main_window_controller.rotateValue.r >= 50

    qtbot.waitUntil(is_rotated)

    assert spy.count() >= 5
    assert main_window_controller.rotateValue.r >= 50
    # Deleting the view before it goes out of scope is required to make sure all child
    # QML instances are destroyed in the correct order.
    del view
