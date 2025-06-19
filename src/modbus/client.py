import traceback
from dataclasses import dataclass
from logging import Logger

from pymodbus import ModbusException
from pymodbus.client import ModbusTcpClient
from pymodbus.pdu import ModbusPDU

from modbus.common import ActionClientInterface


@dataclass
class FuncCallResp:
    """Holds result of a pymodbus function call

    - success: True if no Exception was raised and no error ModbusResponse was returned.
    - val: Value returned from function. Is set to None in error states.
    - err: Traceback of Exception if one occurred, or the text "Modbus error response", or an issue description.
    """

    success: bool
    val: object
    err: str


def pymodbus_call(func, *args, **kwargs) -> FuncCallResp:
    """Wrapper to call pymodbus functions

    Handles catching of Exceptions or error ModbusResponse's
    """
    try:
        resp = func(*args, **kwargs)
    except ModbusException as err:
        return FuncCallResp(False, None, f"Exception in pymodbus: {err}")

    if resp.isError():
        return FuncCallResp(
            False, None, f"Modbus exception, code: {resp.exception_code}"
        )

    return FuncCallResp(True, resp, "")


class ModbusClient(ActionClientInterface):
    action_map = {}

    def __init__(self, log: Logger):
        self.log = log
        super().__init__()
        self.add_action("connect", ModbusClient.connect)
        self.add_action("disconnect", ModbusClient.disconnect)
        self.add_action("raw", ModbusClient.send)

        self.log.debug(f"Built Modbus Client: {dir(ModbusClient)}")
        self.log.debug(f"Actions registered in map: {ModbusClient.action_map}")

    def connect(self, ip: str, port: int = 502, transport: str = "TCP") -> bool:
        """Connect to a PLC

        Args:
            ip (string): IP address of the PLC.
            port (int): Modbus port on the PLC, default: 502.

        Returns:
            success bool
        """
        self.log.info(f"Connecting to {ip}:{port} over {transport}")
        if transport == "TCP":
            self.context.client = ModbusTcpClient(host=ip, port=port)
        else:
            raise NotImplementedError(f"Transport {transport} not implemented")
        self.context.transport = transport

        return self.client.connect()

    def disconnect(self):
        self.log.info("Disconnecting...")
        self.client.close()

    def send(self, payload: bytes) -> FuncCallResp:
        """UNTESTED"""
        self.log.info("[UNTESTED] Sending raw payload over connection")
        return pymodbus_call(self.client.execute, payload)
