import os

import ingenialogger
from ingenialink import CAN_BAUDRATE
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.enums import CanDevice, Connection, Drive
from src.services.motion_controller_service import MotionControllerService
from src.services.types import thread_report

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
        self.connection = Connection.CANopen
        self.can_device = CanDevice.KVASER
        self.baudrate = CAN_BAUDRATE.Baudrate_1M
        self.node_id_l = 31
        self.node_id_r = 32

    @Slot(str)
    def select_dictionary(self, dictionary: str) -> None:
        self.dictionary = dictionary.removeprefix("file:///")
        self.dictionary_changed.emit(os.path.basename(self.dictionary))

    @Slot(int)
    def select_connection(self, connection: int) -> None:
        self.connection = Connection(connection)

    @Slot(int)
    def select_can_device(self, can_device: int) -> None:
        self.can_device = CanDevice(can_device)

    @Slot(int)
    def select_can_baudrate(self, baudrate: int) -> None:
        self.baudrate = CAN_BAUDRATE(baudrate)

    @Slot(int, int)
    def select_node_id(self, node_id: int, drive: int) -> None:
        if drive == Drive.Left.value:
            self.node_id_l = node_id
        else:
            self.node_id_r = node_id

    @Slot()
    def connect(self) -> None:
        self.mcs.connect_drives(
            self.connect_callback,
            self.dictionary,
            self.connection,
            self.can_device,
            self.baudrate,
            self.node_id_l,
            self.node_id_r,
        )

    def connect_callback(self, report: thread_report) -> None:
        if report.exceptions is None:
            self.drive_connected_triggered.emit()
        else:
            self.connection_error_triggered.emit(str(report.exceptions))

    @Slot()
    def disconnect(self) -> None:
        self.mcs.disconnect_drive(self.disconnect_callback)

    def disconnect_callback(self, report: thread_report) -> None:
        if report.exceptions is None:
            self.drive_disconnected_triggered.emit()

    @Slot(float, int)
    def set_velocity(self, velocity: float, drive: int) -> None:
        self.mcs.run(
            self.log_report,
            "motion.set_velocity",
            velocity,
            Drive(drive).name,
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

    @Slot(int)
    def enable_motor(self, drive: int) -> None:
        target = Drive(drive)
        if target == Drive.Left:
            self.mcs.enable_motor(self.enable_motor_l_callback, target)
        else:
            self.mcs.enable_motor(self.enable_motor_r_callback, target)

    @Slot(int)
    def disable_motor(self, drive: int) -> None:
        if drive == Drive.Left.value:
            self.mcs.run(self.disable_motor_l_callback, "motion.motor_enable", drive)
        else:
            self.mcs.run(self.disable_motor_r_callback, "motion.motor_enable", drive)

    def log_report(self, report: thread_report) -> None:
        logger.debug(report)

    def enable_motor_l_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            pollerThread = self.mcs.create_poller_thread(
                Drive.Left.name, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.new_data_available_triggered.connect(self.get_velocities_l)
            pollerThread.start()

    def disable_motor_l_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            self.mcs.stop_poller_thread(Drive.Left.name)

    def enable_motor_r_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            pollerThread = self.mcs.create_poller_thread(
                Drive.Right.name, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
            )
            pollerThread.new_data_available_triggered.connect(self.get_velocities_r)
            pollerThread.start()

    def disable_motor_r_callback(self, report: thread_report) -> None:
        if not report.exceptions:
            self.mcs.stop_poller_thread(Drive.Right.name)
