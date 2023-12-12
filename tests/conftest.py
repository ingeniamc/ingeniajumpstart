import pytest
from controllers.drive_controller import DriveController


@pytest.fixture
def drive_controller() -> DriveController:
    """Fixture to create an instance of DriveController

    Returns:
        DriveController: the DriveController
    """
    return DriveController()
