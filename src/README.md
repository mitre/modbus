# Modbus Plugin Code

Where possible, the Caldera for OT plugins leverage open-source libraries and payloads, unifying their exposure through the Caldera Adversary Emulation framework.

* The Modbus plugin leverages the open-source python library [PyModbus](https://github.com/pymodbus-dev/pymodbus/tree/v2.5.3) - version 2.5.3.

* The PyModbus library v2.5.3 is licensed with the BSD 3-Clause License [license](https://github.com/pymodbus-dev/pymodbus/blob/v2.5.3/LICENSE)

* A custom command-line interface was created by our team for the PyModbus library to allow for Caldera agent interoperability. The CLI payload comes precompiled with the plugin, but can be recompiled following the instructions below.

## Reproducing Builds
The linux payload was compiled with Ubuntu 22.04.2 LTS, Python version 3.8-dev, Pyinstaller 5.10.1.
The windows payload was compiled with Windows 10 v21H2, Python version 3.8.10, Pyinstaller 5.10.1.


## Installation
1. Download source
```sh
git clone <address>
```

2. Optionally create and enter a virtual environment with the required python version above using packages like pyenv, venv, pipenv, or poetry.
```sh
pipenv shell
```
If you need to specify the python version you can use `--python=3.8` in your pipenv command.

3. Install required python packages
```sh
pip install -r ./src/requirements.txt --find-links ./lib/netact/
```

4. Test the CLI
```sh
python ./src/modbus_cli.py -h
```

5. Build the binary with a static builder like pyinstaller or py2exe. Alternatively you can compile the binary with cython. See this stackoverflow thread for more information: [thread](https://stackoverflow.com/questions/39913847/is-there-a-way-to-compile-a-python-application-into-static-binary)
```sh
pyinstaller -F ./src/modbus_cli.py
```

## Testing
The `tests` directory contains [a Modbus Server python script](https://pymodbus.readthedocs.io/en/v2.5.3/source/example/synchronous_server.html) from the PyModbus library that can be used to test all actions included in the plugin.
```sh
python tests/sync_server_ex.py
```
Note: Default port is **5020**
