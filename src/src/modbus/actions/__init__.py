"""
Any files put in the __all__ and imported will be executed on import of the module,
effectively giving them a chance to add additional actions to the ClientInterface object
along with the action_map variable.
"""

__all__ = [
    'proc_modbus',
    'spec'
]

from . import proc_modbus, spec
