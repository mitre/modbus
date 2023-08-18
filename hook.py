from app.utility.base_world import BaseWorld
from plugins.modbus.app.modbus_gui import ModbusGUI
from plugins.modbus.app.modbus_api import ModbusAPI

name = 'Modbus'
description = 'The Modbus plugin for Caldera provides adversary emulation abilities specific to the Modbus control systems protocol.'
address = '/plugin/modbus/gui'
access = BaseWorld.Access.RED


async def enable(services):
    app = services.get('app_svc').application
    modbus_gui = ModbusGUI(services, name=name, description=description)
    app.router.add_static('/modbus', 'plugins/modbus/static/', append_version=True)
    app.router.add_route('GET', '/plugin/modbus/gui', modbus_gui.splash)

    modbus_api = ModbusAPI(services)
    # Add API routes here
    app.router.add_route('POST', '/plugin/modbus/mirror', modbus_api.mirror)

