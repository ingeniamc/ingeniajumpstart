import ingenialogger
from ingeniamotion.metaclass import DEFAULT_SERVO
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.services.motion_controller_service import MotionControllerService
from src.services.types import thread_report

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "qmltypes.controllers"
QML_IMPORT_MAJOR_VERSION = 1

logger = ingenialogger.get_logger(__name__)


@QmlElement
class DriveController(QObject):
    driveConnected: Signal = Signal()
    """Triggers when a drive is connected"""

    driveDisconnected: Signal = Signal()
    """Triggers when a drive is disconnected"""

    velocityValue = Signal(float, float, arguments=["timestamp", "velocity"])
    """Triggers when the poller returns a new value"""

    def __init__(self) -> None:
        super().__init__()
        self.mcs = MotionControllerService()

    @Slot()
    def connect(self) -> None:
        self.mcs.connect_drive(self.connect_callback)

    def connect_callback(self, report: thread_report) -> None:
        logger.debug(report)
        if report.exceptions is None:
            pollerThread = self.mcs.create_poller_thread(
                DEFAULT_SERVO, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.newDataAvailable.connect(self.get_velocities)
            pollerThread.start()
            self.driveConnected.emit()

    @Slot()
    def disconnect(self) -> None:
        self.mcs.disconnect_drive(self.disconnect_callback)

    def disconnect_callback(self, report: thread_report) -> None:
        logger.debug(report)
        if report.exceptions is None:
            self.driveDisconnected.emit()

    @Slot(float)
    def set_velocity(self, velocity: float) -> None:
        self.mcs.run(self.set_velocity_callback, "motion.set_velocity", velocity)

    def set_velocity_callback(self, report: thread_report) -> None:
        logger.debug(report)

    def get_velocities(self, timestamps: list[float], data: list[list[float]]) -> None:
        self.velocityValue.emit(timestamps[0], data[0][0])
