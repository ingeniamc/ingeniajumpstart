import os

import ingenialogger
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.services.motion_controller_service import MotionControllerService
from src.services.types import Connection, Drive, thread_report

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "qmltypes.controllers"
QML_IMPORT_MAJOR_VERSION = 1

logger = ingenialogger.get_logger(__name__)


@QmlElement
class DriveController(QObject):
    drive_connected_triggered: Signal = Signal()
    """Triggers when a drive is connected"""

    drive_disconnected_triggered: Signal = Signal()
    """Triggers when a drive is disconnected"""

    velocity_left_changed = Signal(float, float, arguments=["timestamp", "velocity"])
    """Triggers when the poller returns a new value"""

    velocity_right_changed = Signal(float, float, arguments=["timestamp", "velocity"])
    """Triggers when the poller returns a new value"""

    dictionary_changed = Signal(str, arguments=["dictionary"])
    """Triggers when the dictionary file was selected"""

    connection_error_triggered = Signal(str, arguments=["error_message"])
    """Triggers when the connection failed"""

    def __init__(self) -> None:
        super().__init__()
        self.mcs = MotionControllerService()
        self.connection = Connection.ETHERCAT

    @Slot(str)
    def select_dictionary(self, dictionary: str) -> None:
        self.dictionary = dictionary.removeprefix("file:///")
        self.dictionary_changed.emit(os.path.basename(self.dictionary))

    @Slot(str)
    def select_connection(self, connection: str) -> None:
        if connection == Connection.ETHERCAT.value:
            self.connection = Connection.ETHERCAT
        else:
            self.connection = Connection.CANOPEN

    @Slot()
    def connect(self) -> None:
        self.mcs.connect_drive(self.connect_callback, self.dictionary, self.connection)

    def connect_callback(self, report: thread_report) -> None:
        logger.debug(report)
        if report.exceptions is None:
            self.connection_error_triggered.emit(str(report.exceptions))
        else:
            self.drive_connected_triggered.emit()

    @Slot()
    def disconnect(self) -> None:
        self.mcs.disconnect_drive(self.disconnect_callback)

    def disconnect_callback(self, report: thread_report) -> None:
        logger.debug(report)
        if report.exceptions is None:
            self.drive_disconnected_triggered.emit()

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
        self.velocity_right_changed.emit(timestamps[0], data[0][0])

    def get_velocities_l(
        self, timestamps: list[float], data: list[list[float]]
    ) -> None:
        self.velocity_left_changed.emit(timestamps[0], data[0][0])

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
        if not report.exceptions:
            pollerThread = self.mcs.create_poller_thread(
                Drive.LEFT.value, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.new_data_available_triggered.connect(self.get_velocities_l)
            pollerThread.start()

    def disable_motor_l_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            self.mcs.stop_poller_thread(Drive.LEFT.value)

    def enable_motor_r_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            pollerThread = self.mcs.create_poller_thread(
                Drive.RIGHT.value, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.new_data_available_triggered.connect(self.get_velocities_r)
            pollerThread.start()

    def disable_motor_r_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            self.mcs.stop_poller_thread(Drive.RIGHT.value)
