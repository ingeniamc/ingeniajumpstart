import xml.etree.ElementTree as ET
from functools import partial, wraps
from typing import Any, Callable, Optional, Union

from ingenialink import NET_DEV_EVT, SERVO_STATE
from ingenialink.exceptions import ILError
from ingeniamotion import MotionController
from ingeniamotion.enums import OperationMode
from PySide6.QtCore import QObject, Signal, Slot

from k2basecamp.models.base_model import BaseModel
from k2basecamp.models.bootloader_model import BootloaderModel
from k2basecamp.models.connection_model import ConnectionModel
from k2basecamp.services.motion_controller_thread import MotionControllerThread
from k2basecamp.services.poller_thread import PollerThread
from k2basecamp.utils.enums import ConnectionProtocol, Drive, stringify_can_device_enum
from k2basecamp.utils.types import motion_controller_task, thread_report

DEVICE_NODE = "Body//Device"
INTERFACE_CAN = "CAN"
INTERFACE_ETH = "ETH"
DEFAULT_DICTIONARY_PATH = "k2basecamp/assets/eve-net-c_can_2.4.1.xdf"
EXPECTED_NODE_NR_SCAN = 2
MAX_VELOCITY_REGISTER = "CL_VEL_REF_MAX"
MAX_PROFILER_VELOCITY_REGISTER = "PROF_MAX_VEL"


class MotionControllerService(QObject):
    """
    Service to communicate to the ingeniamotion.MotionController instance. By default
    the communication with the drive should be made using threads.

    """

    error_triggered = Signal(str, arguments=["error_message"])
    """Triggers when an error occurs while communicating with the drive"""

    servo_state_update_triggered: Signal = Signal(Drive, SERVO_STATE)
    """Triggers when the servo state is updated."""

    net_state_update_triggered: Signal = Signal(Drive, NET_DEV_EVT)
    """Triggers when the network state is updated."""

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
        connection_model: ConnectionModel,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        """Connect drives to the program.

        Args:
            report_callback: callback to invoke after
                completing the operation.
            connection_model: model containing the application state.

        Raises:
            ingenialink.exceptions.ILError: If the connection fails
        """

        def on_thread(
            connection_model: ConnectionModel,
        ) -> Any:
            if (
                not connection_model.left_dictionary
                or not connection_model.right_dictionary
            ):
                raise ILError("You need to select a dictionary for each drive.")
            if (
                connection_model.left_dictionary_type != connection_model.connection
                or connection_model.right_dictionary_type != connection_model.connection
            ):
                raise ILError("Communication type does not match the dictionary type.")
            if connection_model.left_id == connection_model.right_id:
                raise ILError("Node IDs cannot be the same.")
            for drive, id, config, dictionary in [
                (
                    Drive.Left,
                    connection_model.left_id,
                    connection_model.left_config,
                    connection_model.left_dictionary,
                ),
                (
                    Drive.Right,
                    connection_model.right_id,
                    connection_model.right_config,
                    connection_model.right_dictionary,
                ),
            ]:
                if id is None:
                    continue
                if connection_model.connection == ConnectionProtocol.EtherCAT:
                    self.__mc.communication.connect_servo_ethercat_interface_index(
                        if_index=self.get_current_interface_index(
                            connection_model.interface
                        ),
                        slave_id=id,
                        dict_path=dictionary,
                        alias=drive.name,
                        servo_status_listener=True,
                        net_status_listener=True,
                    )
                elif connection_model.connection == ConnectionProtocol.CANopen:
                    self.__mc.communication.connect_servo_canopen(
                        baudrate=connection_model.can_baudrate,
                        can_device=stringify_can_device_enum(
                            connection_model.can_device
                        ),
                        dict_path=dictionary,
                        node_id=id,
                        alias=drive.name,
                        servo_status_listener=True,
                        net_status_listener=True,
                    )
                else:
                    raise ILError("Connection type not implemented.")

                self.__mc.communication.subscribe_servo_status(
                    partial(self.servo_status_callback, drive), drive.name
                )
                self.__mc.communication.subscribe_net_status(
                    partial(self.net_status_callback, drive), drive.name
                )
                if config is not None:
                    self.__mc.configuration.load_configuration(
                        config_path=config, servo=drive.name
                    )

        return on_thread

    def servo_status_callback(
        self, drive: Drive, state: SERVO_STATE, _: None, subnode: int
    ) -> None:
        """Callback when the state of the drive changes

        Args:
            drive: the affected drive
            state: the new state
            _ (None): (unused)
            subnode: subnode, unused
        """
        self.servo_state_update_triggered.emit(drive, state)

    def net_status_callback(self, drive: Drive, state: NET_DEV_EVT) -> None:
        """Callback when the state of the network changes

        Args:
            drive: the affected drive
            state: the new state
        """
        self.net_state_update_triggered.emit(drive, state)

    def get_interface_name_list(self) -> list[str]:
        """Get a list of available interface names from the MotionController.

        Returns:
            list[str]: list of interfaces
        """
        return self.__mc.communication.get_interface_name_list()

    def get_current_interface_index(self, interface: Optional[str]) -> int:
        if interface is None:
            raise ILError("Interface is not set.")
        available_interfaces = self.__mc.communication.get_interface_name_list()
        return available_interfaces.index(interface)

    @run_on_thread
    def scan_servos(
        self,
        report_callback: Callable[[thread_report], Any],
        base_model: BaseModel,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., list[int]]:
        """Scan for servos in the network.

        Args:
            report_callback: callback to invoke after
                completing the operation.
            base_model: Contains information about the connection
            minimum_nodes: the minimum number of nodes we expect to find (e.g.
                installing firmware only requires one, while connect to drives needs
                two).

        Raises:
            ingenialink.exceptions.ILError: If we find less than the expected number of
                servos in the network or the connection protocol is not implemented.

        Returns:
            list[int]: All slave / node IDs that are found.
        """

        def on_thread(base_model: BaseModel) -> list[int]:
            if base_model.connection == ConnectionProtocol.CANopen:
                result = self.__mc.communication.scan_servos_canopen(
                    can_device=stringify_can_device_enum(base_model.can_device),
                    baudrate=base_model.can_baudrate,
                )
            elif base_model.connection == ConnectionProtocol.EtherCAT:
                result = self.__mc.communication.scan_servos_ethercat_interface_index(
                    self.get_current_interface_index(base_model.interface)
                )
            else:
                raise ILError("Connection type not implemented.")
            if len(result) < EXPECTED_NODE_NR_SCAN:
                nodes_found = result if len(result) > 0 else "(none)"
                raise ILError(
                    f"Scan expected to find at least {EXPECTED_NODE_NR_SCAN} nodes. "
                    + f"Nodes found: {nodes_found}"
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
        """Disconnect the drives if they are connected.

        Args:
            report_callback: callback to invoke after
                completing the operation.
        """

        def on_thread() -> Any:
            for servo in list(self.__mc.servos):
                if self.__mc.is_alive(servo):
                    self.__mc.motion.motor_disable(servo=servo)
                    self.stop_poller_thread(servo)
                    self.__mc.communication.disconnect(servo=servo)

        return on_thread

    @run_on_thread
    def emergency_stop(
        self,
        report_callback: Callable[[thread_report], Any],
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        """Disable the motors of the drives that are connected.

        Args:
            report_callback: callback to invoke after
                completing the operation.
        """

        def on_thread() -> Any:
            for servo in self.__mc.servos:
                if self.__mc.is_alive(servo):
                    self.__mc.motion.motor_disable(servo=servo)
                    self.stop_poller_thread(servo)

        return on_thread

    @Slot()
    def execute_callback(
        self, callback: Callable[..., Any], thread_report: thread_report
    ) -> None:
        """Helper function to execute a callback function. Used when the
        MotionControllerThread sends the task_completed signal.

        Args:
            callback: the callback to execute
            thread_report: the thread_report that serves as parameter to
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
            alias:  Drive alias.
            registers: Register to be read.
            sampling_time: Poller sampling time. Defaults to 0.125.
            refresh_time: Poller refresh period. Defaults to 0.125.
            buffer_size: Poller buffer size. Defaults to 100.

        Returns:
            PollerThread: the newly created PollerThread
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
        """Stop the poller thread for the given drive."""
        if alias in self.__poller_threads and self.__poller_threads[alias].isRunning():
            self.disconnect(self.__poller_threads[alias])
            self.__poller_threads[alias].stop()
            self.__poller_threads[alias].quit()

    def check_dictionary_format(self, filepath: str) -> ConnectionProtocol:
        """Identifies if the provided dictionary file is for CANopen or
        ETHERcat connections.

        Args:
            filepath: path to the file to check

        Raises:
            ingenialink.exceptions.ILError: If the provided file has the wrong format
            FileNotFoundError: If the file was not found

        Returns:
            utils.enums.ConnectionProtocol: The connection type the file is meant for.
        """
        tree = ET.parse(filepath)
        parsed_data = tree.getroot()

        device = parsed_data.find(DEVICE_NODE)
        if not isinstance(device, ET.Element):
            raise ILError("Invalid file format")
        interface = device.attrib["Interface"]
        if interface == INTERFACE_CAN:
            return ConnectionProtocol.CANopen
        elif interface == INTERFACE_ETH:
            return ConnectionProtocol.EtherCAT
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
        """Enables the motor of a given drive

        Args:
            report_callback: callback to invoke after
                completing the operation.
            drive: the drive to enable
        """

        def on_thread(drive: Drive) -> Any:
            self.__mc.motion.set_operation_mode(
                OperationMode.PROFILE_VELOCITY, servo=drive.name
            )
            self.__mc.motion.motor_enable(servo=drive.name)

        return on_thread

    def stop_motion_controller_thread(self) -> None:
        """Stops the MotionControllerThread that was created upon initialization."""
        self.disconnect(self.__motion_controller_thread)
        self.__motion_controller_thread.stop()
        self.__motion_controller_thread.quit()
        self.__motion_controller_thread.wait()

    @run_on_thread
    def install_firmware(
        self,
        report_callback: Callable[[thread_report], Any],
        progress_callback: Callable[[int], Any],
        bootloader_model: BootloaderModel,
        firmware: str,
        left_id: int,
        right_id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        """Install firmware to a given drive.

        Args:
            report_callback: callback to invoke after completing the operation.
            progress_callback: callback for when the installation progress updates.
            bootloader_model: the model with the application state.
            firmware: the file containing the firmware.
            left_id: the node id of the left drive.
            right_id: the node id of the right drive.
        """

        def on_thread(
            progress_callback: Callable[[int], Any],
            bootloader_model: BootloaderModel,
            firmware: str,
            left_id: int,
            right_id: int,
        ) -> Any:
            if not bootloader_model.install_prerequisites_met():
                self.error_triggered.emit(
                    "Incorrect or insufficient configuration. Make sure to provide the "
                    + "right parameters for the selected connection protocol."
                )
                return

            if bootloader_model.connection == ConnectionProtocol.CANopen:
                self.__mc.communication.connect_servo_canopen(
                    baudrate=bootloader_model.can_baudrate,
                    can_device=stringify_can_device_enum(bootloader_model.can_device),
                    dict_path=DEFAULT_DICTIONARY_PATH,
                    node_id=left_id,
                    alias=Drive.Left.name,
                )
                self.__mc.communication.connect_servo_canopen(
                    baudrate=bootloader_model.can_baudrate,
                    can_device=stringify_can_device_enum(bootloader_model.can_device),
                    dict_path=DEFAULT_DICTIONARY_PATH,
                    node_id=right_id,
                    alias=Drive.Right.name,
                )
                # We pass one of the two drive aliases to the function. It should
                # automatically detect that we have a two drive setup based on the
                # firmware file type and update both drives.
                self.__mc.communication.load_firmware_canopen(
                    servo=Drive.Left.name,
                    fw_file=firmware,
                    progress_callback=progress_callback,
                )
                self.__mc.communication.disconnect(servo=Drive.Left.name)
                self.__mc.communication.disconnect(servo=Drive.Right.name)
            elif bootloader_model.connection == ConnectionProtocol.EtherCAT:
                self.__mc.communication.load_firmware_ecat_interface_index(
                    fw_file=firmware,
                    if_index=self.get_current_interface_index(
                        bootloader_model.interface
                    ),
                    slave=left_id,
                )

        return on_thread

    @run_on_thread
    def set_max_velocity(
        self,
        report_callback: Callable[[thread_report], Any],
        drive: Drive,
        max_velocity: float,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        """Set the maximum velocity of the given drive. There are two registers that
        have an effect on this property - we are simply setting them both to the given
        value to keep things simple in this application.

        Args:
            report_callback: callback to invoke after
                completing the operation.
            drive: the target drive.
            max_velocity: the new maximum velocity.

        """

        def on_thread(drive: Drive, max_velocity: float) -> Any:
            self.__mc.communication.set_register(
                MAX_VELOCITY_REGISTER, max_velocity, drive.name
            )
            self.__mc.communication.set_register(
                MAX_PROFILER_VELOCITY_REGISTER, max_velocity, drive.name
            )

        return on_thread

    @run_on_thread
    def get_last_error_message(
        self,
        report_callback: Callable[[thread_report], Any],
        drive: Drive,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        """Get the last error of a given drive.

        Args:
            report_callback: callback to invoke after
                completing the operation.
            drive: the target drive.

        """

        def on_thread(drive: Drive) -> Any:
            error_code, *_ = self.__mc.errors.get_last_buffer_error(servo=drive.name)
            *_, error_msg = self.__mc.errors.get_error_data(
                error_code, servo=drive.name
            )
            return error_msg

        return on_thread

    @run_on_thread
    def get_number_of_errors(
        self,
        report_callback: Callable[[thread_report], Any],
        drive: Drive,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        """Get the total number of errors of a given drive.

        Args:
            report_callback: callback to invoke after
                completing the operation.
            drive: the target drive.

        """

        def on_thread(drive: Drive) -> Any:
            num_current_errors = self.__mc.errors.get_number_total_errors(servo=drive.name)
            return drive, num_current_errors

        return on_thread

