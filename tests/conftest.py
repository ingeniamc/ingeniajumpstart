import pytest

from src.controllers.main_window_console import MainWindowConsole
from src.controllers.main_window_controller import MainWindowController


@pytest.fixture
def main_window_controller() -> MainWindowController:
    return MainWindowController()


@pytest.fixture
def main_window_console() -> MainWindowConsole:
    return MainWindowConsole()
