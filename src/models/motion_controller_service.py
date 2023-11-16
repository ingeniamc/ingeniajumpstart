from functools import wraps
from typing import Any, Callable, Union

from ingeniamotion import MotionController
from ingeniamotion.enums import CAN_DEVICE, OperationMode
from PySide6.QtCore import QObject

from .mc_thread import MCThread
from .poller_thread import PollerThread
from .types import Drive, thread_report


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
    def connect_drive(
        self,
        report_callback: Callable[[thread_report], Any],
        *args: Any,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def on_thread() -> Any:
            """
            [docs]

            """
            self.__mc.communication.connect_servo_canopen(
                CAN_DEVICE.KVASER,
                "eve-xcr-c_can_2.4.1.xdf",
                31,
                alias=Drive.LEFT.value,
            )
            self.__mc.communication.connect_servo_canopen(
                CAN_DEVICE.KVASER,
                "eve-xcr-c_can_2.4.1.xdf",
                32,
                alias=Drive.RIGHT.value,
            )

            # self.__mc.communication.connect_servo_eoe(
            #    "192.168.2.22", "eve-e-xcr-c_eth_2.4.1.xdf"
            # )
            self.__mc.motion.set_operation_mode(
                OperationMode.PROFILE_VELOCITY, servo=Drive.LEFT.value
            )
            self.__mc.motion.set_operation_mode(
                OperationMode.PROFILE_VELOCITY, servo=Drive.RIGHT.value
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
            self.__mc.motion.motor_disable(servo=Drive.LEFT.value)
            self.stop_poller_thread(Drive.LEFT.value)
            self.__mc.communication.disconnect(servo=Drive.LEFT.value)
            self.__mc.motion.motor_disable(servo=Drive.RIGHT.value)
            self.stop_poller_thread(Drive.RIGHT.value)
            self.__mc.communication.disconnect(servo=Drive.RIGHT.value)

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
