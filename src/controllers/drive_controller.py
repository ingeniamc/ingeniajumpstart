import os
from typing import Union

import ingenialogger
from ingenialink import CAN_BAUDRATE
from PySide6.QtCore import QJsonArray, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.enums import CanDevice, ConnectButtonState, Connection, Drive
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

    error_triggered = Signal(str, arguments=["error_message"])
    """Triggers when an error occurs while communicating with the drive"""

    connect_button_state_changed = Signal(int, arguments=["button_state"])
    """Triggers when the state of the connect button changes"""

    servo_ids_changed = Signal(QJsonArray, arguments=["servo_ids"])
    """Triggers when the scan returned new values for the servo connections"""

    def __init__(self) -> None:
        super().__init__()
        self.mcs = MotionControllerService()
        self.mcs.error_triggered.connect(self.error_message_callback)
        self.connection = Connection.CANopen
        self.can_device = CanDevice.KVASER
        self.baudrate = CAN_BAUDRATE.Baudrate_1M
        self.left_id: Union[int, None] = None
        self.right_id: Union[int, None] = None
        self.interface_index = 0
        self.dictionary: Union[str, None] = None
        self.dictionary_type: Union[Connection, None] = None

    def update_connect_button_state(self) -> None:
        self.connect_button_state_changed.emit(
            self.connect_button_state_canopen().value
        )

    def connect_button_state_canopen(self) -> ConnectButtonState:
        if (
            self.dictionary is None
            or self.dictionary_type is None
            or self.connection != self.dictionary_type
            or self.left_id is None
            or self.right_id is None
            or self.left_id == self.right_id
            or (
                self.connection == Connection.CANopen
                and (self.can_device is None or self.baudrate is None)
            )
            or (
                self.connection == Connection.EtherCAT
                and (self.interface_index is None)
            )
        ):
            return ConnectButtonState.Disabled
        return ConnectButtonState.Enabled

    def error_message_callback(self, error_message: str) -> None:
        self.error_triggered.emit(error_message)
        self.update_connect_button_state()

    @Slot(str)
    def select_dictionary(self, dictionary: str) -> None:
        self.dictionary = dictionary.removeprefix("file:///")
        self.dictionary_type = self.mcs.check_dictionary_format(self.dictionary)
        self.dictionary_changed.emit(os.path.basename(self.dictionary))
        self.update_connect_button_state()

    @Slot(int)
    def select_connection(self, connection: int) -> None:
        self.connection = Connection(connection)
        self.update_connect_button_state()

    @Slot(int)
    def select_interface(self, interface: int) -> None:
        self.interface_index = interface
        self.update_connect_button_state()

    @Slot(int)
    def select_can_device(self, can_device: int) -> None:
        self.can_device = CanDevice(can_device)
        self.update_connect_button_state()

    @Slot(int)
    def select_can_baudrate(self, baudrate: int) -> None:
        self.baudrate = CAN_BAUDRATE(baudrate)
        self.update_connect_button_state()

    @Slot(int, int)
    def select_node_id(self, node_id: int, drive: int) -> None:
        if drive == Drive.Left.value:
            self.left_id = node_id
        else:
            self.right_id = node_id
        self.update_connect_button_state()

    @Slot()
    def connect(self) -> None:
        self.mcs.connect_drives(
            self.connect_callback,
            self.dictionary,
            self.connection,
            self.can_device,
            self.baudrate,
            self.left_id,
            self.right_id,
            self.interface_index,
        )

    def connect_callback(self, report: thread_report) -> None:
        self.drive_connected_triggered.emit()

    @Slot()
    def disconnect(self) -> None:
        self.mcs.disconnect_drives(self.disconnect_callback)

    def disconnect_callback(self, report: thread_report) -> None:
        self.drive_disconnected_triggered.emit()
        self.update_connect_button_state()

    @Slot(float, int)
    def set_velocity(self, velocity: float, drive: int) -> None:
        self.mcs.run(
            self.log_report,
            "motion.set_velocity",
            velocity,
            servo=Drive(drive).name,
        )

    @Slot()
    def get_velocities_r(
        self, timestamps: list[float], data: list[list[float]]
    ) -> None:
        self.velocity_right_changed.emit(timestamps[0], data[0][0])

    @Slot()
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
            self.mcs.run(
                self.disable_motor_l_callback,
                "motion.motor_disable",
                Drive.Left.name,
            )
        else:
            self.mcs.run(
                self.disable_motor_r_callback,
                "motion.motor_disable",
                Drive.Right.name,
            )

    def log_report(self, report: thread_report) -> None:
        logger.debug(report)

    def enable_motor_l_callback(self, report: thread_report) -> None:
        poller_thread = self.mcs.create_poller_thread(
            Drive.Left.name, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
        )
        poller_thread.new_data_available_triggered.connect(self.get_velocities_l)
        poller_thread.start()

    def disable_motor_l_callback(self, report: thread_report) -> None:
        self.mcs.stop_poller_thread(Drive.Left.name)

    def enable_motor_r_callback(self, report: thread_report) -> None:
        poller_thread = self.mcs.create_poller_thread(
            Drive.Right.name, [{"name": "CL_VEL_FBK_VALUE", "axis": 1}]
        )
        poller_thread.new_data_available_triggered.connect(self.get_velocities_r)
        poller_thread.start()

    def disable_motor_r_callback(self, report: thread_report) -> None:
        self.mcs.stop_poller_thread(Drive.Right.name)

    @Slot(result=QJsonArray)
    def get_interface_name_list(self) -> QJsonArray:
        return QJsonArray.fromStringList(self.mcs.get_interface_name_list())

    @Slot()
    def scan_servos(self) -> None:
        self.mcs.scan_servos(
            self.scan_servos_callback,
            self.connection,
            self.can_device,
            self.baudrate,
            self.interface_index,
        )

    def scan_servos_callback(self, thread_report: thread_report) -> None:
        if thread_report.output is not None:
            servo_ids: list[int] = thread_report.output
            self.left_id = servo_ids[0]
            self.right_id = servo_ids[1]
            self.servo_ids_changed.emit(QJsonArray.fromVariantList(servo_ids))
            self.update_connect_button_state()
