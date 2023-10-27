from typing import Union

from PySide6.QtCore import QObject


class Console(QObject):
    """Output stuff on the console."""

    def output(self, s: Union[str, float]) -> None:
        print(s)

    def outputStr(self, s: str) -> None:
        print(s)

    def outputFloat(self, x: float) -> None:
        print(x)
