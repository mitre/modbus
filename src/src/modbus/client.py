import traceback
from logging import Logger
from dataclasses import dataclass

from pymodbus.pdu import ModbusResponse

from pymodbus.client.sync import ModbusTcpClient
from modbus.common import ActionClientInterface


@dataclass
class FuncCallResp:
    """Holds results gotten from calling a pymodbus function

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
        val = func(*args, **kwargs)
    except Exception:
        err = traceback.format_exc()
        return FuncCallResp(False, None, err)

    if isinstance(val, ModbusResponse) and val.isError():
        return FuncCallResp(False, None, "Modbus error response")

    return FuncCallResp(True, val, "")


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

    def connect(self, ip: str, port: int = 502, transport: str = "TCP") -> FuncCallResp:
        """Connect to a PLC

        Args:
            ip (string): IP address of the PLC.
            port (int): Modbus port on the PLC, default: 502.

        Returns:
            FuncCallResp data object as a dict
        """
        self.log.info(f"Connecting to {ip}:{port} over {transport}")
        if transport == "TCP":
            self.context.client = ModbusTcpClient(ip, port)
        else:
            raise NotImplementedError(f"Transport {transport} not implemented")
        self.context.transport = transport
        ret = pymodbus_call(self.client.connect)

        return {"success": ret.success, "err": ret.err}

    def disconnect(self) -> FuncCallResp:
        self.log.info("Disconnecting...")
        ret = pymodbus_call(self.client.close)

        return {"success": ret.success, "err": ret.err}

    def send(self, payload: bytes) -> FuncCallResp:
        """UNTESTED"""
        self.log.info("[UNTESTED] Sending raw payload over connection")
        ret = pymodbus_call(self.client.execute, payload)

        return {"success": ret.success, "err": ret.err, "response": ret.val}
