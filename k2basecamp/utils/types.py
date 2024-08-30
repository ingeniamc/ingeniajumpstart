from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Optional, Union

from k2basecamp.utils.enums import Drive


@dataclass
class thread_report:
    """Type for thread reports that are returned by threads. They contain information
    about the execution result of the thread."""

    drive: Optional[Drive]
    method: str
    output: Optional[Any]
    timestamp: float
    duration: float
    exceptions: Optional[Exception]


@dataclass
class motion_controller_task:
    """Type for a task that a MotionControllerThread should execute. Contains the action
    (i.e. function) to perform, its arguments, and a callback function to call after
    completing the action.
    """

    action: Callable[..., Any]
    callback: Union[Callable[..., Any], partial[Callable[..., Any]]]
    args: Any
    kwargs: Any
