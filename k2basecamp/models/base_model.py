from typing import Optional

from ingenialink import CAN_BAUDRATE
from PySide6.QtCore import QObject

from k2basecamp.utils.enums import CanDevice, ConnectionProtocol


class BaseModel(QObject):
    """Holds the state of the application.
    Is created and manipulated by the ConnectionController.
    """

    def __init__(
        self,
        connection: ConnectionProtocol = ConnectionProtocol.CANopen,
        can_device: CanDevice = CanDevice.KVASER,
        can_baudrate: CAN_BAUDRATE = CAN_BAUDRATE.Baudrate_1M,
        interface: Optional[str] = None,
        left_id: Optional[int] = None,
        right_id: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.connection = connection
        self.can_device = can_device
        self.can_baudrate = can_baudrate
        self.interface = interface
        self.left_id = left_id
        self.right_id = right_id
