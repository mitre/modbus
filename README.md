# Caldera for OT plugin: Modbus

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying
[Caldera](https://github.com/mitre/caldera) with Modbus protocol TTPs. This is
part of a series of plugins that provide added threat emulation capability for
Operational Technology (OT) environments.

Full Modbus plugin [documentation](docs/modbus.md) can be viewed as part of
fieldmanual, once the Caldera server is running.

## Installation

To run Caldera along with modbus plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install the modbus plugin in Caldera's plugin directory: `caldera/plugins`
3. Enable the modbus plugin by adding `- modbus` to the list of enabled plugins
   in `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure
   mode)

### Payload Compatibility

This plugin uses pre-compiled binaries (payloads) that are delivered and
executed on the target device by the Caldera agent. To execute, the payloads 
must be compatible with the target device operating system. For more information 
on compatibility, see the [fieldmanual documention](/docs/modbus.md#payloads) and 
the [source README](/src/README.md). 


### Payload Source Code

For additional information on the modbus plugin payload source code, please see
the [source directory](/src/), which contains additional licensing and
build guidance.

## Usage

1. **Select Your Target System**  
   Determine the system you want to communicate with via the Modbus protocol.
   This could be an industrial control system, a programmable logic controller
   (PLC), or any other Modbus-compatible device.

2. **Choose a Host for the Caldera Agent**  
   Identify a suitable machine to host the Caldera agent. This machine will act
   as the intermediary, sending Modbus messages to your target system. Ensure the
   host has network access to the target system and meets the deployment
   requirements.

3. **Deploy the Caldera Agent**  
   Deploy the Caldera agent to the chosen host. Instructions and scripts to 
   acheive this are found on the Caldera server GUI on the "Agents" page. 

4. **Execute Modbus Plugin Abilities**  
   Utilize the Modbus plugin's abilities to perform specific actions on the
   target system. Combine abilities such as reading registers and writing 
   coils to achieve your desired outcome.

For detailed instructions and ability descriptions, see the
[fieldmanual documention](/docs/modbus.md#usage).

### Virtual Test Device: [Wildcat Dam](https://github.com/mitre/wildcatdam)

To help you test the Modbus plugin without any additional hardware
requirements, we provide a virtual Modbus device called **Wildcat Dam**. This
simulated dam controller mimics the behavior of a real-world Modbus device,
allowing you to test the plugin and build your understanding of the Modbus
protocol without needing access to physical hardware.

To get started, follow the instructions [here](https://github.com/mitre/wildcatdam).

