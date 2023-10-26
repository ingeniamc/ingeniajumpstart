from PySide6.QtCore import QObject, Signal


class Rotate(QObject):
    """Used to rotate an element in the frontend

    Args:
        QObject (Shiboken.Object): Marks this class as a QObject
    """

    valueChanged = Signal(int, arguments=["val"])

    def __init__(self) -> None:
        super().__init__()
        self.r = 0

    def increment(self) -> None:
        """Changes the rotation and emits a signal to the frontend."""
        self.r = self.r + 10
        self.valueChanged.emit(self.r)
