from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from models.console import Console

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "qmltypes.controllers"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MainWindowConsole(QObject):
    console: Console

    def __init__(self) -> None:
        super().__init__()
        self.console = Console()

    @Slot(str)
    @Slot(float)
    def output(self, s: str | float) -> None:
        self.console.output(s)

    @Slot(str)
    def outputStr(self, s: str) -> None:
        self.console.outputStr(s)

    @Slot(float)
    def outputFloat(self, x: float) -> None:
        self.console.outputFloat(x)
