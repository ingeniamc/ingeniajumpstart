from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class thread_report:
    method: str
    output: Optional[Any]
    timestamp: float
    duration: float
    exceptions: Optional[Exception]
