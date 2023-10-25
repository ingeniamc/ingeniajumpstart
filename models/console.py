from PySide6.QtCore import QObject


class Console(QObject):
    """Output stuff on the console."""

    def output(self, s: str | float) -> None:
        print(s)

    def outputStr(self, s: str) -> None:
        print(s)

    def outputFloat(self, x: float) -> None:
        print(x)
