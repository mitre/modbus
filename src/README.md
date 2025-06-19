# Modbus Plugin Code

Where possible, the Caldera for OT plugins leverage open-source libraries and
payloads, unifying their exposure through the Caldera Adversary Emulation
framework.

- The Modbus plugin leverages the open-source python library
  [PyModbus](https://github.com/pymodbus-dev/pymodbus/tree/v3.9.2) - version
  3.9.2.

- The PyModbus library v3.9.2 is licensed with the BSD 3-Clause License
  [license](https://github.com/pymodbus-dev/pymodbus/blob/v3.9.2/LICENSE)

- A custom command-line interface was created by our team for the PyModbus
  library to allow for Caldera agent interoperability. The CLI payload comes
  precompiled with the plugin, but can be recompiled following the instructions
  below.

## Building with PyInstaller

The payloads for this plugin were built with PyInstaller. This creates *relatively*
static payloads, allowing them to be passed to a target machine and executed without
issue. However, the process of compiling python code into a single binary is an 
imperfect process. One known dependency is that the Linux version of the payload
was built with `glibc` version 2.31. This makes the payload compatible with 
versions of Linux that have a `glibc` greater than or equal to 2.31. 


The most successful way to ensure the payload is compatible with a particular
device is to build the payload in that environment by following the steps below.

1. Install [PyInstaller](https://pyinstaller.org/en/latest/installation.html)

2. From the `src/` directory, execute PyInstaller:
```sh
make build/local
```

3. Copy the newly built binary to the `payloads/` directory so that it is detected
   and used by Caldera.
```sh 
cp dist/modbus_cli(.exe) ../payloads 
```

**Note**: The `Makefile` also includes targets to build the payloads in Docker 
containers. This is how the distributed payloads were built.


## Testing

`pymodbus` includes example servers that provide and excellent test interface 
for the abilities in this plugin. Follow the instructions in the 
[`pymodbus` documentation](https://pymodbus.readthedocs.io/en/latest/source/examples.html)
to run the test server.
