import xml.etree.ElementTree as ET
from functools import wraps
from typing import Any, Callable, Union

from ingenialink import CAN_BAUDRATE
from ingenialink.exceptions import ILError
from ingeniamotion import MotionController
from ingeniamotion.enums import OperationMode
from PySide6.QtCore import QObject

from src.enums import CanDevice, Connection, Drive, stringify_can_device_enum

from .mc_thread import MCThread
from .poller_thread import PollerThread
from .types import (
    thread_report,
)

DEVICE_NODE = "Body//Device"
INTERFACE_CAN = "CAN"
INTERFACE_ETH = "ETH"


class MotionControllerService(QObject):
    """
    Service to communicate to the ingeniamotion.MotionController instance. By default
    the communication with the drive should be made using threads.

    """

    def __init__(self) -> None:
        """The constructor for MotionControllerService class"""
        super().__init__()
        self.__threads: dict[int, MCThread] = {}
        self.__total_threads: int = 0
        self.__mc: MotionController = MotionController()
        self.registers_cache: dict[str, dict[int, dict[str, Any]]] = {}
        self.__poller_threads: dict[str, PollerThread] = {}

    def run(
        self,
        report_callback: Callable[[thread_report], None],
        command: Union[Callable[..., Any], str],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Run an ingeniamotion method or a custom method in a thread. The thread is
        removed once it finishes.

        Args:
            report_callback: When the thread finishes, the report is sent back emitting
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

        thread_id = self.__total_threads
        self.__total_threads += 1
        thread = MCThread(method, thread_id, *args, **kwargs)

        thread.thread_finished.connect(self.remove_thread)
        thread.thread_report.connect(report_callback)

        self.__threads[thread_id] = thread
        thread.start()

    def remove_thread(self, thread_id: int) -> None:
        """Remove a thread

        Args:
            thread_id: Thread identifier.

        """
        if self.__threads[thread_id].isRunning():
            self.__threads[thread_id].wait()
        self.__threads.pop(thread_id)

    def run_on_thread(func: Callable[..., Any]) -> Callable[..., None]:  # type: ignore
        """
        Decorator that runs a method on a thread. To use this decorator, an inner
        function should be included and returned in the function to be wrapped (`func`).
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
        node_id_l: int,
        node_id_r: int,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread(
            dictionary: str,
            connection: Connection,
            can_device: CanDevice,
            baudrate: CAN_BAUDRATE,
            node_id_l: int,
            node_id_r: int,
        ) -> Any:
            """Connect drives to the program.

            Args:
                dictionary (str): dictionary file used for the connection
                connection (Connection): whether to connect via ETHERcat or CANopen

            Raises:
                ILError: If the connection fails
            """
            dictionary_type = self.__check_dictionary_format(dictionary)
            if dictionary_type != connection:
                raise ILError("Communication type does not match the dictionary type.")
            if connection == Connection.EtherCAT:
                raise ILError("Not (yet) implemented.")
            if node_id_l == node_id_r:
                raise ILError("Node IDs cannot be the same.")

            self.__mc.communication.connect_servo_canopen(
                baudrate=baudrate,
                can_device=stringify_can_device_enum(can_device),
                dict_path=dictionary,
                node_id=node_id_l,
                alias=Drive.Left.name,
            )
            self.__mc.communication.connect_servo_canopen(
                baudrate=baudrate,
                can_device=stringify_can_device_enum(can_device),
                dict_path=dictionary,
                node_id=node_id_r,
                alias=Drive.Right.name,
            )

        return on_thread

    @run_on_thread
    def disconnect_drive(
        self,
        report_callback: Callable[[thread_report], Any],
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread() -> Any:
            """
            [docs]

            """
            self.__mc.motion.motor_disable(servo=Drive.Left.name)
            self.stop_poller_thread(Drive.Left.name)
            self.__mc.communication.disconnect(servo=Drive.Left.name)
            self.__mc.motion.motor_disable(servo=Drive.Right.name)
            self.stop_poller_thread(Drive.Right.name)
            self.__mc.communication.disconnect(servo=Drive.Right.name)

        return on_thread

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

    def __check_dictionary_format(self, filepath: str) -> Connection:
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
            self.__mc.motion.set_operation_mode(
                OperationMode.PROFILE_VELOCITY, servo=drive.name
            )
            self.__mc.motion.motor_enable(servo=drive.name)

        return on_thread
