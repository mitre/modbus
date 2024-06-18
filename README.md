# Caldera for OT plugin: Modbus

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying [Caldera](https://github.com/mitre/caldera) with Modbus protocol TTPs.
This is part of a series of plugins that provide added threat emulation capability for Operational Technology (OT) environments.

Full Modbus plugin [documentation](docs/modbus.md) can be viewed as part of fieldmanual, once the Caldera server is running.

## Installation

To run Caldera along with modbus plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install the modbus plugin in Caldera's plugin directory: `caldera/plugins`
3. Enable the modbus plugin by adding `- modbus` to the list of enabled plugins in `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure mode)

### Version
This plugin is compatible with Caldera version 4.2.0 and version 5.0.0. The latest version of Caldera can be checked out using the following method:
```
git clone --recursive https://github.com/mitre/caldera.git
```
### Tested OS Versions for Plugin Payload(s)

Building of the Modbus plugin payloads has been tested as described [here](/src/README.md#reproducing-builds). See the corresponding plugin payload source code for further build information.

Testing of the binaries has occured on:
* Microsoft Windows 10 v21H2
* Ubuntu 22.04.2 LTS

#### Plugin Payload Source Code

For additional information on the modbus plugin payload source code, please see [this corresponding repository](/src/), which contains additional licensing and build guidance.

## Plugin Usage
 - Import the plugin, and optionally set up the required facts (i.e. like the fact sources provided).
 - Start an operation, optionally using the fact source you set up.
 - Use "Add Potential Link" to run a specific ability from this plugin. You can enter the fact values manually, or use the ones from your fact source.
 
 Sources contains a small [example fact set](/data/sources/0033b644-a615-4eff-bcf3-178e9b17adc3.yml) and the fieldmanual documentation contains a reference section on [modbus sources.](/docs/modbus.md#modbus-sources-and-facts)