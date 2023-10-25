from PySide6.QtCore import QObject, Signal


class Rotate(QObject):
    valueChanged = Signal(int, arguments=["val"])

    def __init__(self) -> None:
        super().__init__()
        self.r = 0

    def increment(self) -> None:
        self.r = self.r + 10
        self.valueChanged.emit(self.r)
