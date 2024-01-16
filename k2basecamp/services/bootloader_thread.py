from typing import Any, Callable

import ingenialogger
from ingeniamotion import MotionController
from PySide6.QtCore import QThread, Signal

from k2basecamp.models.bootloader_model import BootloaderModel
from k2basecamp.utils.enums import Drive

logger = ingenialogger.get_logger(__name__)


class BootloaderThread(QThread):
    """Thread to install firmware."""

    firmware_installation_complete_triggered = Signal()
    """Triggers when the installation of firmware files was completed successfully."""

    firmware_installation_progress_changed = Signal(int, arguments=["progress"])
    """During installation, information about the progress of the operation is emitted.

    Args:
        progress (int): The progress as a percentage.
    """

    error_triggered = Signal(str, arguments=["error_message"])
    """Triggers when an error occurs while communicating with the drive.

    Args:
        error_message (str): the error message.
    """

    def __init__(
        self,
        install_firmware: Callable[
            [Drive, Callable[[int], Any], BootloaderModel, str, int, MotionController],
            None,
        ],
        drive: Drive,
        bootloader_model: BootloaderModel,
        firmware: str,
        id: int,
        mc: MotionController,
    ) -> None:
        super().__init__()
        self.__install_firmware = install_firmware
        self.__drive = drive
        self.__bootloader_model = bootloader_model
        self.__firmware = firmware
        self.__id = id
        self.__mc = mc

    def run(self) -> None:
        """Start the thread."""
        try:
            self.__install_firmware(
                self.__drive,
                self.progress_callback,
                self.__bootloader_model,
                self.__firmware,
                self.__id,
                self.__mc,
            )
            self.firmware_installation_complete_triggered.emit()
        except Exception as e:
            logger.error(e)
            self.error_triggered.emit(str(e))

    def progress_callback(self, progress: int) -> None:
        self.firmware_installation_progress_changed.emit(progress)
