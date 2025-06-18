# Modbus

Modbus Protocol Threat Emulation Tooling

## Overview
The Modbus plugin provides adversary emulation abilities specific to the Modbus protocol. The specification for the Modbus protocol is free and available to download from the Modbus organization at [modbus.org](https:www.modbus.org/specs.php) The following table outlines MITRE ATT&CK for ICS Tactic coverage provided by the Modbus plugin.

|[Collection](#collection-abilities)| [Impair Process Control](#impair-process-control-abilities) |
|:-------------------------|:----------------------|
|Point & Tag Identification| Brute Force I/O |
|                          | Modify Parameter |


### Ability Overview Tables
The following tables list each plugin ability by their corresponding tactic. A heatmap of plugin abilities is available to view [here](assets/heatmap.png).

#### Collection Abilities
| Name 	   | Tactic | Technique |  Technique ID   |
|----------|--------|-----------|-----------------|
|[Modbus - Read Coils](#modbus---read-coils)  |Collection  |Point & Tag Identification  |T0861  |
|[Modbus - Read Discrete Inputs](#modbus---read-discrete-inputs)  |Collection  |Point & Tag Identification  |T0861  |
|[Modbus - Read Holding Registers](#modbus---read-holding-registers)  |Collection  |Point & Tag Identification  |T0861  |
|[Modbus - Read Input Registers](#modbus---read-input-registers)  |Collection  |Point & Tag Identification  |T0861  |

#### Impair Process Control Abilities
| Name 	                | Tactic 	        | Technique |  Technique ID     |
|----------             |---------          |-----------|----------         |
|[Modbus - Write Single Coil](#modbus---write-single-coil)  |Impair Process Control  | Modify Parameter  |T0836  |
|[Modbus - Write Single Register](#modbus---write-single-register)  |Impair Process Control  | Modify Parameter  |T0836  |
|[Modbus - Write Multiple Coils](#modbus---write-multiple-coils) |Impair Process Control  | Brute Force I/O  |T0806  |
|[Modbus - Write Multiple Registers](#modbus---write-multiple-registers)  |Impair Process Control  | Brute Force I/O  |T0806  |
|[Modbus - Fuzz Coils](#modbus---fuzz-coils)  |Impair Process Control  | Brute Force I/O  |T0806  |
|[Modbus - Fuzz Registers](#modbus---fuzz-registers)  |Impair Process Control  | Brute Force I/O  |T0806  |

## Architecture

This section describes the main components of the plugin and how they interface.
### Block Diagram
![block diagram](assets/modbus_diagram.jpg)

The Modbus Plugin allows a user to execute several abilities once added to the Caldera instance. The abilities will be executed via the Caldera agent and corresponding payload. This is intended to target devices communicating via the Modbus protocol, likely over port 502.

### Payloads

The Modbus Plugin includes one payload, compiled for two different host architectures: 
- `modbus_cli.exe` (Windows)
- `modbus_cli` (Linux)

#### Compatibility

The payloads were compiled in the following environments:

|            | Linux | Windows |
|------------|-------|---------|
| OS Version | Linux-6.8.0-60-generic-x86_64-with-glibc2.31 | Windows-10-10.0.19043-SP0 |
| Python Version | 3.13.3 | 3.13.3 |
| PyInstaller | 6.13.0 | 6.13.0 |


### Libraries
The following libraries were used to build the Modbus payloads:
| Library | Version	 | License |
|---------|--------- |---------|
|pymodbus |[3.9.2](https://github.com/pymodbus-dev/pymodbus/tree/v3.9.2) |[BSD](https://github.com/pymodbus-dev/pymodbus/blob/v3.9.2/LICENSE)      |


## Usage
This section describes how to initially deploy and execute the abilities present within the Modbus plugin.

### Deployment

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

```{tip}
Reference the Caldera training plugin for a step-by-step tutorial on how to
deploy an agent and run abilities via an operation.
```

### Modbus Sources and Facts

Caldera fact sources allow you to save information about your target environment
to simplify executing abilities. This plugin comes with a sample fact source
named "Modbus Sample Facts" that will have loaded with the plugin. Navigate to
the Sources tab of the Caldera interface to view and modify these facts.

### Abilities
#### Modbus - Read Coils
Modbus Function 1 (0x01): Read Coils

This function code is used to read from 1 to 2000 contiguous states of coils in a
remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} read_c #{modbus.read_coil.start} #{modbus.read_coil.count}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} read_c #{modbus.read_coil.start} #{modbus.read_coil.count}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.read_coil.start` | The starting address to read from | int | 0-65535 |
| `modbus.read_coil.count` | The number of items to read | int  | 1-2000 |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Read Discrete Inputs
Modbus Function 2 (0x02): Read Discrete Inputs

This function code is used to read from 1 to 2000 contiguous discrete inputs
in a remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} read_di #{modbus.read_discrete.start} #{modbus.read_discrete.count}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} read_di #{modbus.read_discrete.start} #{modbus.read_discrete.count}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.read_discrete.start` | The starting address to read from | int | 0-65535 |
| `modbus.read_discrete.count` | The number of items to read | int  | 1-2000 |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Read Holding Registers
Modbus Function 3 (0x03): Read Holding Registers

This function code is used to read the contents of a contiguous block of holding
registers in a remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} read_hr #{modbus.read_holding.start} #{modbus.read_holding.count}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} read_hr #{modbus.read_holding.start} #{modbus.read_holding.count}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.read_holding.start` | The starting address to read from | int | 0-65535 |
| `modbus.read_holding.count` | The number of items to read | int  | 1-125 |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |


#### Modbus - Read Input Registers
Modbus Function 4 (0x04): Read Input Registers

This function code is used to read from 1 to 125 contiguous input registers in a
remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} read_ir #{modbus.read_input.start} #{modbus.read_input.count}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} read_ir #{modbus.read_input.start} #{modbus.read_input.count}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.read_input.start` | The starting address to read from | int | 0-65535 |
| `modbus.read_input.count` | The number of items to read | int  | 1-125 |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Write Single Coil
Modbus Function 5 (0x05): Write Single Coil

This function code is used to write a single output to either ON or OFF in a
remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} write_c #{modbus.write_coil.start} #{modbus.write_coil.value}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} write_c #{modbus.write_coil.start} #{modbus.write_coil.value}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.write_coil.start` | The starting address to write to | int | 0-65535 |
| `modbus.write_coil.value` | The value to be written | str  | ON,OFF |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Write Single Register
Modbus Function 6 (0x06): Write Single Register

This function code is used to write a single holding register in a remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} write_r #{modbus.write_register.start} #{modbus.write_register.value}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} write_r #{modbus.write_register.start} #{modbus.write_register.value}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.write_register.start` | The starting address to write to | int | 0-65535 |
| `modbus.write_register.value` | The value to be written | int  | 0-65535 |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Write Multiple Coils
Modbus Function 15 (0x0F): Write Multiple Coils

This function code is used to force each coil in a sequence of coils to either
ON or OFF in a remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} write_multi_c #{modbus.write_coil.start} #{modbus.write_coil.values}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} write_multi_c #{modbus.write_coil.start} #{modbus.write_coil.values}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.write_coil.start` | The starting address to write to | int | 0-65535 |
| `modbus.write_coil.values` | The values to be written | comma separated list of str  | ON,OFF |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Write Multiple Registers
Modbus Function 16 (0x10): Write Multiple Registers

This function code is used to write a block of contiguous registers
(1 to 123 registers) in a remote device.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} write_multi_r #{modbus.write_register.start} #{modbus.write_register.values}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} write_multi_r #{modbus.write_register.start} #{modbus.write_register.values}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.write_register.start` | The starting address to write to | int | 0-65535 |
| `modbus.write_register.values` | The values to be written | comma separated list of int  | 0-65535 |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Fuzz Coils
Procedure  
Modbus Function 5 (0x05) Write Single Coil

Writes random values to random coils over specified ranges.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} fuzz_c #{modbus.fuzz_coil.start} #{modbus.fuzz_coil.end} #{modbus.fuzz_coil.count} --wait #{modbus.fuzz_coil.wait}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} fuzz_c #{modbus.fuzz_coil.start} #{modbus.fuzz_coil.end} #{modbus.fuzz_coil.count} --wait #{modbus.fuzz_coil.wait}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.fuzz_coil.start` | The start address of the fuzzing range | int | 0-65535 |
| `modbus.fuzz_coil.end` | The end address of the fuzzing range | int | 0-65535 |
| `modbus.fuzz_coil.count` | The number of write operations to perform | int | 0-65535 |
| `modbus.fuzz_coil.wait` | Seconds to wait between write operations | float |  |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

#### Modbus - Fuzz Registers
Procedure  
Modbus Function 6 (0x06): Write Single Register

Writes random values to random registers over specified ranges.

__Ability Command:__
<details open>
<summary>Windows (psh)</summary>
<br>

```caldera
.\modbus_cli.exe #{modbus.server.ip} -p #{modbus.server.port} fuzz_r #{modbus.fuzz_register.start} #{modbus.fuzz_register.end} #{modbus.fuzz_register.count} --min #{modbus.fuzz_register.min} --max #{modbus.fuzz_register.max} --wait #{modbus.fuzz_register.wait}
```  

</details>
<details>
<summary>Linux (sh)</summary>
<br>

```caldera
./modbus_cli #{modbus.server.ip} -p #{modbus.server.port} fuzz_r #{modbus.fuzz_register.start} #{modbus.fuzz_register.end} #{modbus.fuzz_register.count} --min #{modbus.fuzz_register.min} --max #{modbus.fuzz_register.max} --wait #{modbus.fuzz_register.wait}
```  

</details>
<br>

__Facts:__  
| Name | Description | Type | Choices |
|:-----|:------------|:----:|:-------:|
| `modbus.server.ip` | The target device IP address | string |  |
| `modbus.server.port` | The target device Modbus port | int |  |
| `modbus.fuzz_register.start` | The start address of the fuzzing range | int | 0-65535 |
| `modbus.fuzz_register.end` | The end address of the fuzzing range | int | 0-65535 |
| `modbus.fuzz_register.count` | The number of write operations to perform | int | 0-65535 |
| `modbus.fuzz_register.min` | Minimum register write value | int | 0-65535 |
| `modbus.fuzz_register.max` | Maximum register write value | int | 0-65535 |
| `modbus.fuzz_register.wait` | Seconds to wait between write operations | float |  |

__Optional Flags:__
| Flag | Description | Type | Default |
|:-----|:------------|:----:|:-------:|
| `-d`, `--device` | Device ID to be targeted [0-255] | int | 1 |

## Source Code
The source code for the Modbus plugin can be found inside this plugin's `src/` directory.

## Copyright Notice
Modbus® is a registered trademark of SCHNEIDER ELECTRIC USA, INC. CORPORATION DELAWARE 1415 SOUTH ROSELLE ROAD PALATINE ILLINOIS 60067

This Caldera plugin is named "Modbus" as that is a short identifier of its purpose / scope. This plugin is not produced-by Schneider Electric or The Modbus Corporation.
