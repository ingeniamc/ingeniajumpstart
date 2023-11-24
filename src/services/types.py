from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class thread_report:
    method: str
    output: Optional[Any]
    timestamp: float
    duration: float
    exceptions: Optional[Exception]


@dataclass
class motion_controller_task:
    action: Callable[..., Any]
    callback: Callable[..., Any]
    args: Any
    kwargs: Any
