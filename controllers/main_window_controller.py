from PySide6.QtCore import QObject, Signal
from PySide6.QtQml import QmlElement

from models.rotate import Rotate

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "qmltypes.controllers"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MainWindowController(QObject):
    valueChanged = Signal(int, arguments=["val"])

    rotateValue: Rotate

    def __init__(self) -> None:
        super().__init__()
        self.rotateValue = Rotate()
        # self.console = Console()
        self.connect_view_and_model()

    def connect_view_and_model(self) -> None:
        self.rotateValue.valueChanged.connect(self.valueChanged)

    def rotate(self) -> None:
        self.rotateValue.increment()
