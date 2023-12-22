from typing import Generator

import pytest

from src.controllers.drive_controller import DriveController


@pytest.fixture
def drive_controller() -> Generator[DriveController, None, None]:
    drive_controller = DriveController()
    yield drive_controller
    drive_controller.mcs.stop_motion_controller_thread()
