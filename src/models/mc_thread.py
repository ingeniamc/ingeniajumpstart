import time
from typing import Any, Callable

from ingenialink.exceptions import (
    ILError,
)
from ingeniamotion.exceptions import IMException
from PySide6.QtCore import QThread, Signal

from .types import thread_report


class MCThread(QThread):
    """
    Thread to run ingeniamotion native functions or custom functions defined in the
    MotionControllerService.

    """

    thread_started: Signal = Signal()
    """Signal emitted when the thread starts"""

    thread_finished: Signal = Signal(int)
    """Signal emitted when the thread finishes.
    The thread_id is returned by the thread"""

    thread_report: Signal = Signal(thread_report)
    """Signal emitted when the thread finishes.
    A report [thread_report] is returned by the thread"""

    def __init__(
        self, callback: Callable[..., Any], thread_id: int, *args: Any, **kwargs: Any
    ) -> None:
        """
        The constructor for MCThread class

        Args:
            callback: Function to run in the thread.
            thread_id: Thread identifier.
            args: Positional arguments to pass to the callback function.
            kwargs: Optional arguments to pass to the callback function.

        """
        self.__callback = callback
        self.__thread_id = thread_id
        self.__args = args
        self.__kwargs = kwargs
        super().__init__()

    def run(self) -> None:
        """Run function.
        Emit a signal when it starts (started) and when finishes (finished). Besides,
        emits a report of :class:`~motionlab3.dataclasses.thread_report` type using
        the report signal. This report includes the method name, the output of the
        callback function, a timestamp, the duration and the exception raised during
        the callback, if any.

        """
        timestamp = time.time()
        self.thread_started.emit()
        raised_exception = None
        output = None
        try:
            output = self.__callback(*self.__args, **self.__kwargs)
        except (IMException, ILError, ValueError, KeyError, FileNotFoundError) as e:
            raised_exception = e
        duration = time.time() - timestamp
        report = thread_report(
            self.__callback.__qualname__, output, timestamp, duration, raised_exception
        )
        self.thread_report.emit(report)
        self.thread_finished.emit(self.__thread_id)
