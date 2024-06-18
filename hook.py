from app.utility.base_world import BaseWorld
from plugins.modbus.app.modbus_svc import ModbusService

name = 'Modbus'
description = 'The Modbus plugin for Caldera provides adversary emulation abilities specific to the Modbus control systems protocol.'
address = '/plugin/modbus/gui'
access = BaseWorld.Access.RED


async def enable(services):
    modbus_svc = ModbusService(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/modbus/gui', modbus_svc.splash)
    app.router.add_route('GET', '/plugin/modbus/data', modbus_svc.plugin_data)
    
