from PySide6.QtCore import QObject, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement

from src.models.motion_controller_service import MotionControllerService
from src.models.types import Drive, thread_report

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "qmltypes.controllers"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class DriveController(QObject):
    driveConnected: Signal = Signal()
    """Triggers when a drive is connected"""

    driveDisconnected: Signal = Signal()
    """Triggers when a drive is disconnected"""

    velocityLeft = Signal(float, float, arguments=["timestamp", "velocity"])
    """Triggers when the poller returns a new value"""

    velocityRight = Signal(float, float, arguments=["timestamp", "velocity"])
    """Triggers when the poller returns a new value"""

    def __init__(self) -> None:
        super().__init__()
        self.mcs = MotionControllerService()
        self.value = 0
        self.timer = QTimer()

    @Slot()
    def connect(self) -> None:
        self.mcs.connect_drive(self.connect_callback)

    def connect_callback(self, report: thread_report) -> None:
        print(report)
        if not report.exceptions:
            self.driveConnected.emit()

    @Slot()
    def disconnect(self) -> None:
        self.mcs.disconnect_drive(self.disconnect_callback)

    def disconnect_callback(self, report: thread_report) -> None:
        print(report)
        if not report.exceptions:
            self.driveDisconnected.emit()

    @Slot(float, str)
    def set_velocity(self, velocity: float, drive: str) -> None:
        self.mcs.run(
            self.generic_callback,
            "motion.set_velocity",
            velocity,
            drive,
        )

    def get_velocities_r(
        self, timestamps: list[float], data: list[list[float]]
    ) -> None:
        print(timestamps, data)
        self.velocityRight.emit(timestamps[0], data[0][0])

    def get_velocities_l(
        self, timestamps: list[float], data: list[list[float]]
    ) -> None:
        print(timestamps, data)
        self.velocityLeft.emit(timestamps[0], data[0][0])

    @Slot(str)
    def enable_motor(self, drive: str) -> None:
        if drive == Drive.LEFT.value:
            self.mcs.run(self.enable_motor_l_callback, "motion.motor_enable", drive)
        else:
            self.mcs.run(self.enable_motor_r_callback, "motion.motor_enable", drive)

    @Slot(str)
    def disable_motor(self, drive: str) -> None:
        if drive == Drive.LEFT.value:
            self.mcs.run(self.disable_motor_l_callback, "motion.motor_enable", drive)
        else:
            self.mcs.run(self.disable_motor_r_callback, "motion.motor_enable", drive)

    def generic_callback(self, report: thread_report) -> None:
        print(report)

    def enable_motor_l_callback(self, report: thread_report) -> None:
        print(report)
        if not report.exceptions:
            pollerThread = self.mcs.create_poller_thread(
                Drive.LEFT.value, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.newDataAvailable.connect(self.get_velocities_l)
            pollerThread.start()

    def disable_motor_l_callback(self, report: thread_report) -> None:
        print(report)
        if not report.exceptions:
            self.mcs.stop_poller_thread(Drive.LEFT.value)

    def enable_motor_r_callback(self, report: thread_report) -> None:
        print(report)
        if not report.exceptions:
            pollerThread = self.mcs.create_poller_thread(
                Drive.RIGHT.value, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.newDataAvailable.connect(self.get_velocities_r)
            pollerThread.start()

    def disable_motor_r_callback(self, report: thread_report) -> None:
        print(report)
        if not report.exceptions:
            self.mcs.stop_poller_thread(Drive.RIGHT.value)
