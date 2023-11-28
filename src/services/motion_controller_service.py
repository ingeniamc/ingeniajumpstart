import xml.etree.ElementTree as ET
from functools import wraps
from typing import Any, Callable, Union

from ingenialink import CAN_BAUDRATE
from ingenialink.exceptions import ILError
from ingeniamotion import MotionController
from ingeniamotion.enums import OperationMode
from PySide6.QtCore import QObject, Signal, Slot

from src.enums import CanDevice, Connection, Drive, stringify_can_device_enum
from src.services.motion_controller_thread import MotionControllerThread

from .poller_thread import PollerThread
from .types import motion_controller_task, thread_report

DEVICE_NODE = "Body//Device"
INTERFACE_CAN = "CAN"
INTERFACE_ETH = "ETH"


class MotionControllerService(QObject):
    """
    Service to communicate to the ingeniamotion.MotionController instance. By default
    the communication with the drive should be made using threads.

    """

    error_triggered = Signal(str, arguments=["error_message"])
    """Triggers when an error occurs while communicating with the drive"""

    def __init__(self) -> None:
        """The constructor for MotionControllerService class"""
        super().__init__()
        self.__mc: MotionController = MotionController()
        self.registers_cache: dict[str, dict[int, dict[str, Any]]] = {}
        self.__poller_threads: dict[str, PollerThread] = {}
        # Create a thread to communicate with the drive
        self.__motion_controller_thread = MotionControllerThread()
        self.__motion_controller_thread.task_completed.connect(self.execute_callback)
        self.__motion_controller_thread.task_errored.connect(self.error_triggered)
        self.__motion_controller_thread.start()

    def run(
        self,
        report_callback: Callable[[thread_report], None],
        command: Union[Callable[..., Any], str],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Add an ingeniamotion method or a custom method to the MotionControllerThread
        task queue.

        Args:
            report_callback: When the task finishes, the report is sent back emitting
                a signal to the callback.
            command: Method to run in the thread. Could be either a ingeniamotion method
                using a str including the module and method name, e.g.,
                "communication.get_register" or a callable function, for instance,
                self.get_register.
            args: Positional arguments to pass to the command function.
            kwargs: Optional arguments to pass to the command function.

        """
        if isinstance(command, str):
            module_name, method_name = command.split(".")
            module = getattr(self.__mc, module_name)
            method = getattr(module, method_name)
        else:
            method = command

        thread = self.__motion_controller_thread
        thread.queue.put(
            motion_controller_task(
                action=method,
                callback=report_callback,
                args=args,
                kwargs=kwargs,
            )
        )

    def run_on_thread(func: Callable[..., Any]) -> Callable[..., None]:  # type: ignore
        """
        Decorator that wraps a method to be passed to the MotionControllerThread. To use
        this decorator, an inner function should be included and returned in the
        function to be wrapped (`func`).
        This inner function includes everything that runs in the thread. The `func`
        signature should be always the same:
        `function_name(self, report_callback, *args, **kwargs)`. See an example below:

        .. code-block:: python

            @run_on_thread
            def get_register(self, report_callback, *args, **kwargs):

                def on_thread(*args, **kwargs):
                    self.__mc.communication.get_register(*args, **kwargs)

                return on_thread


        Args:
            func: function to be wrapped.

        Returns:
            Wrapped function.
        """

        @wraps(func)
        def wrap(self: "MotionControllerService", *args: Any, **kwargs: Any) -> None:
            on_thread = func(self, *args, **kwargs)
            self.run(args[0], on_thread, *args[1:], **kwargs)

        return wrap

    @run_on_thread
    def connect_drives(
        self,
        report_callback: Callable[[thread_report], Any],
        dictionary: str,
        connection: Connection,
        can_device: CanDevice,
        baudrate: CAN_BAUDRATE,
        id_l: int,
        id_r: int,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread(
            dictionary: str,
            connection: Connection,
            can_device: CanDevice,
            baudrate: CAN_BAUDRATE,
            id_l: int,
            id_r: int,
            interface_index: int,
        ) -> Any:
            """Connect drives to the program.

            Args:
                dictionary (str): dictionary file used for the connection
                connection (Connection): whether to connect via ETHERcat or CANopen
                can_device (CanDevice): configuration for CANopen
                baudrate (CAN_BAUDRATE): configuration for CANopen
                id_l (int): configuration for CANopen
                id_r (int): configuration for CANopen

            Raises:
                ILError: If the connection fails
            """
            dictionary_type = self.check_dictionary_format(dictionary)
            if dictionary_type != connection:
                raise ILError("Communication type does not match the dictionary type.")
            if id_l == id_r:
                raise ILError("Node IDs cannot be the same.")
            if connection == Connection.EtherCAT:
                self.connect_drives_ethercat(
                    interface_index,
                    dictionary,
                    id_l,
                    id_r,
                )
            elif connection == Connection.CANopen:
                self.connect_drives_canopen(
                    dictionary, can_device, baudrate, id_l, id_r
                )
            else:
                raise ILError("Connection type not implemented.")

        return on_thread

    def connect_drives_ethercat(
        self, interface_index: int, dictionary: str, id_l: int, id_r: int
    ) -> None:
        self.__mc.communication.connect_servo_ethercat_interface_index(
            if_index=interface_index,
            slave_id=id_l,
            dict_path=dictionary,
            alias=Drive.Left.name,
        )
        self.__mc.communication.connect_servo_ethercat_interface_index(
            if_index=interface_index,
            slave_id=id_r,
            dict_path=dictionary,
            alias=Drive.Right.name,
        )

    def connect_drives_canopen(
        self,
        dictionary: str,
        can_device: CanDevice,
        baudrate: CAN_BAUDRATE,
        id_l: int,
        id_r: int,
    ) -> None:
        self.__mc.communication.connect_servo_canopen(
            baudrate=baudrate,
            can_device=stringify_can_device_enum(can_device),
            dict_path=dictionary,
            node_id=id_l,
            alias=Drive.Left.name,
        )
        self.__mc.communication.connect_servo_canopen(
            baudrate=baudrate,
            can_device=stringify_can_device_enum(can_device),
            dict_path=dictionary,
            node_id=id_r,
            alias=Drive.Right.name,
        )

    def get_interface_name_list(self) -> list[str]:
        return self.__mc.communication.get_interface_name_list()  # type: ignore

    @run_on_thread
    def scan_servos(
        self,
        report_callback: Callable[[thread_report], Any],
        connection: Connection,
        can_device: CanDevice,
        baudrate: CAN_BAUDRATE,
        interface_index: int,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread(
            connection: Connection,
            can_device: CanDevice,
            baudrate: CAN_BAUDRATE,
            interface_index: int,
        ) -> Any:
            result = []
            if connection == Connection.CANopen:
                result = self.__mc.communication.scan_servos_canopen(
                    can_device=stringify_can_device_enum(can_device), baudrate=baudrate
                )
            elif connection == Connection.EtherCAT:
                result = self.__mc.communication.scan_servos_ethercat_interface_index(
                    interface_index
                )
            else:
                raise ILError("Connection type not implemented.")
            if len(result) != 2:
                nodes_found = result if len(result) > 0 else "(none)"
                raise ILError(
                    f"Scan expected to find exactly 2 nodes. Nodes found: {nodes_found}"
                )
            return result

        return on_thread

    @run_on_thread
    def disconnect_drives(
        self,
        report_callback: Callable[[thread_report], Any],
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread() -> Any:
            """Disconnect the drives if they are connected."""
            for servo in [Drive.Left.name, Drive.Right.name]:
                if self.__mc.is_alive(servo):
                    self.__mc.motion.motor_disable(servo=servo)
                    self.stop_poller_thread(servo)
                    self.__mc.communication.disconnect(servo=servo)

        return on_thread

    @Slot()
    def execute_callback(
        self, callback: Callable[..., Any], thread_report: thread_report
    ) -> None:
        """Helper function to execute a callback function. Used when the
        MotionControllerThread sends the task_completed signal.

        Args:
            callback (Callable[..., Any]): the callback to execute
            thread_report (thread_report): the thread_report that serves as parameter to
                the callback function.
        """
        callback(thread_report)

    def create_poller_thread(
        self,
        alias: str,
        registers: list[dict[str, Union[int, str]]],
        sampling_time: float = 0.125,
        refresh_time: float = 0.125,
        buffer_size: int = 100,
    ) -> PollerThread:
        """Create an instance of the PollerThread.

        Args:
            alias: Drive alias.
            registers: Register to be read.
            sampling_time: Poller sampling time.
            refresh_time: Poller refresh period.
            buffer_size: Poller buffer size.
        """
        self.__poller_threads[alias] = PollerThread(
            self.__mc,
            alias,
            registers,
            sampling_time=sampling_time,
            refresh_time=refresh_time,
            buffer_size=buffer_size,
        )
        return self.__poller_threads[alias]

    def stop_poller_thread(self, alias: str) -> None:
        """Stop poller thread."""
        if alias in self.__poller_threads and self.__poller_threads[alias].isRunning():
            self.__poller_threads[alias].stop()

    def check_dictionary_format(self, filepath: str) -> Connection:
        """Identifies if the provided dictionary file is for CANopen or
        ETHERcat connections.

        Args:
            filepath (str): path to the file to check

        Raises:
            ILError: If the provided file has the wrong format
            FileNotFoundError: If the file was not found

        Returns:
            Connection: The connection type the file is meant for.
        """
        tree = ET.parse(filepath)
        parsed_data = tree.getroot()

        device = parsed_data.find(DEVICE_NODE)
        if not isinstance(device, ET.Element):
            raise ILError("Invalid file format")
        interface = device.attrib["Interface"]
        if interface == INTERFACE_CAN:
            return Connection.CANopen
        elif interface == INTERFACE_ETH:
            return Connection.EtherCAT
        else:
            raise ILError("Connection type not supported.")

    @run_on_thread
    def enable_motor(
        self,
        report_callback: Callable[[thread_report], Any],
        drive: Drive,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread(drive: Drive) -> Any:
            """Enables the motor of a given drive

            Args:
                drive (Drive): The drive

            """
            self.__mc.motion.set_operation_mode(
                OperationMode.PROFILE_VELOCITY, servo=drive.name
            )
            self.__mc.motion.motor_enable(servo=drive.name)

        return on_thread
