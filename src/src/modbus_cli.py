import logging
import argparse
import modbus.version
from modbus.client import ModbusClient


FORMAT = "%(asctime)-15s %(levelname)-8s %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


def is_16bit_uint(value):
    ivalue = int(value)
    if(ivalue < 0 or ivalue > 65535):
        raise argparse.ArgumentTypeError("%s is an invalid 16bit uint." % value)
    return ivalue


def add_unit_arg(parser):
    parser.add_argument(
        "-U", "--unit",
        dest="unit",
        type=int,
        required=False,
        default=1,
        help="Slave unit to be targeted [0-255]"
    )


def add_common_write_args(parser):
    parser.add_argument(
        "start",
        type=is_16bit_uint,
        help="The starting address to write to [0-65535]"
    )
    parser.add_argument(
        "value",
        type=int,
        metavar="value",
        choices=[0, 1],
        help="The value to be written where 0=OFF 1=ON [0,1]"
    )


def add_common_write_r_args(parser):
    parser.add_argument(
        "start",
        type=is_16bit_uint,
        help="The starting address to write to, addressing starts at 0 [0-65535]"
    )
    parser.add_argument(
        "value",
        type=is_16bit_uint,
        help="The value to be written [0-65535]"
    )


def add_common_write_mask_r_args(parser):
    parser.add_argument(
        "start",
        type=is_16bit_uint,
        help="The starting address to write to, addressing starts at 0 [0-65535]"
    )
    parser.add_argument(
        "andmask",
        type=is_16bit_uint,
        help="The value of the AND mask [0-65535]",
    )
    parser.add_argument(
        "ormask",
        type=is_16bit_uint,
        help="The value of the OR mask [0-65535]",
    )


def add_common_read_args(parser):
    parser.add_argument(
        "start",
        type=is_16bit_uint,
        help="The starting address to read from [0-65535]"
    )
    parser.add_argument(
        "count",
        type=is_16bit_uint,
        help="The number of items to read [0-65535]"
    )


def add_common_fuzz_args(parser):
    parser.add_argument(
        "start",
        type=is_16bit_uint,
        help="The start address of the fuzzing range [0-65535]"
    )
    parser.add_argument(
        "end",
        type=is_16bit_uint,
        help="The end address of the fuzzing range [0-65535]"
    )
    add_unit_arg(parser)
    parser.add_argument(
        "count",
        type=is_16bit_uint,
        help="Number of write operations to perform [0-65535]",
    )
    parser.add_argument(
        "--wait",
        dest="wait",
        type=float,
        required=False,
        default=0.0,
        help="Seconds to wait between write operations [>= 0.0]",
    )


def add_write_c_subparser(subparsers):
    parser = subparsers.add_parser(
        "write_c",
        help="Write Single Coil: Write to a single specified coil")
    add_common_write_args(parser)
    add_unit_arg(parser)


def add_write_multi_c_subparser(subparsers):
    parser = subparsers.add_parser(
        "write_multi_c",
        help="Write Multiple Coils: Write to a specified range of coils")
    add_common_write_args(parser)
    parser.add_argument(
        "count",
        type=is_16bit_uint,
        help="The number of coils to be written to [0-65535]"
    )
    add_unit_arg(parser)


def add_read_c_subparser(subparsers):
    parser = subparsers.add_parser(
        "read_c",
        help="Read Coils: Read the status values for the specified coils")
    add_common_read_args(parser)
    add_unit_arg(parser)


def add_read_di_subparser(subparsers):
    parser = subparsers.add_parser(
        "read_di",
        help="Read Discrete Input: Read the status values for the specified discrete inputs")
    add_common_read_args(parser)
    add_unit_arg(parser)


def add_write_r_subparser(subparsers):
    parser = subparsers.add_parser(
        "write_r",
        help="Write Single Register: Write to a single specified register")
    add_common_write_r_args(parser)
    add_unit_arg(parser)


def add_write_multi_r_subparser(subparsers):
    parser = subparsers.add_parser(
        "write_multi_r",
        help="Write Multiple Registers: Write to a specified range of registers")
    add_common_write_r_args(parser)
    parser.add_argument(
        "count",
        type=is_16bit_uint,
        help="The number of registers to be written to [0-65535]"
    )
    add_unit_arg(parser)


def add_mask_write_r_subparser(subparsers):
    parser = subparsers.add_parser(
        "mask_write_r",
        help="Mask Write Register: Modifies contents of a single register using AND or OR mask")
    add_common_write_mask_r_args(parser)
    add_unit_arg(parser)


def add_read_hr_subparser(subparsers):
    parser = subparsers.add_parser(
        "read_hr",
        help="Read Holding Registers: Read the status values for the specified holding registers")
    add_common_read_args(parser)
    add_unit_arg(parser)


def add_read_ir_subparser(subparsers):
    parser = subparsers.add_parser(
        "read_ir",
        help="Read Input Registers: Read the status values for the specified input registers")
    add_common_read_args(parser)
    add_unit_arg(parser)


def add_fuzz_c_subparser(subparsers):
    parser = subparsers.add_parser(
        "fuzz_c",
        help="Fuzz Coils: Randomly write coils")
    add_common_fuzz_args(parser)


def add_fuzz_r_subparser(subparsers):
    parser = subparsers.add_parser(
        "fuzz_r",
        help="Fuzz Registers: Randomly write registers")
    add_common_fuzz_args(parser)
    parser.add_argument(
        "--min",
        dest="min",
        type=is_16bit_uint,
        required=False,
        default=0,
        help="Minimum register write value [0-65535]",
    )
    parser.add_argument(
        "--max",
        dest="max",
        type=is_16bit_uint,
        required=False,
        default=65535,
        help="Maximum register write value [0-65535]",
    )


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Modbus Client Action Library " + modbus.version.get_version())

    parser.add_argument("ip", help="The target device IP address")
    parser.add_argument(
        "-p", "--port",
        dest="port",
        default="502",
        help="The target device Modbus port [0-65535]"
    )

    subparsers = parser.add_subparsers(help="Action to be taken", required=True, dest="action")
    add_write_c_subparser(subparsers)
    add_write_multi_c_subparser(subparsers)
    add_read_c_subparser(subparsers)
    add_read_di_subparser(subparsers)
    add_fuzz_c_subparser(subparsers)
    add_fuzz_r_subparser(subparsers)
    add_read_hr_subparser(subparsers)
    add_read_ir_subparser(subparsers)
    add_write_r_subparser(subparsers)
    add_write_multi_r_subparser(subparsers)
    add_mask_write_r_subparser(subparsers)

    return parser


def do_action(client, args):

    if args.action.lower() == "read_di":
        log.info("[*] Read discrete inputs")
        try:
            result = client.read_discrete_inputs(args.start, args.count, args.unit)
        except Exception as err:
            log.info(err)
        else:
            print_table(result, args.start, args.count, "bit")

    elif args.action.lower() == "read_c":
        log.info("[*] Read coils")
        fptr = client.get("read_coils")
        try:
            result = fptr(client, args.start, args.count, args.unit)
        except Exception as err:
            log.info(err)
        else:
            print_table(result, args.start, args.count, "bit")

    elif args.action.lower() == "read_hr":
        log.info("[*] Read holding registers")
        try:
            result = client.read_holding_registers(args.start, args.count, args.unit)
        except Exception as err:
            log.info(err)
        else:
            print_table(result, args.start, args.count, "register")

    elif args.action.lower() == "read_ir":
        log.info("[*] Read input registers")
        try:
            result = client.read_input_registers(args.start, args.count, args.unit)
        except Exception as err:
            log.info(err)
        else:
            print_table(result, args.start, args.count, "register")

    elif args.action.lower() == "write_c":
        log.info("[*] Write coil")
        result = client.write_coil(args.start, args.value, args.unit)
        if result.isError():
            log.info("Write error.")
        else:
            log.info("Write successful.")

    elif args.action.lower() == "write_multi_c":
        log.info("[*] Write multiple coils")
        result = client.write_coils(args.start, args.value, args.count, args.unit)
        if result.isError():
            log.info("Write error.")
        else:
            log.info("Write successful.")

    elif args.action.lower() == "write_r":
        log.info("[*] Write single register")
        result = client.write_register(args.start, args.value, args.unit)
        if result.isError():
            log.info("Write error.")
        else:
            log.info("Write successful.")

    elif args.action.lower() == "write_multi_r":
        log.info("[*] Write multiple registers")
        result = client.write_registers(args.start, args.value, args.count, args.unit)
        if result.isError():
            log.info("Write error.")
        else:
            log.info("Write successful.")

    elif args.action.lower() == "mask_write_r":
        log.info("[*] Mask write single register")
        result = client.mask_write_register(args.start, args.andmask, args.ormask, args.unit)
        if result.isError():
            log.info("Write error.")
        else:
            log.info("Write successful.")

    elif args.action.lower() == "fuzz_c":
        log.info("[*] Randomly fuzz coils:")
        try:
            result = client.fuzz_coils(args.start, args.end, args.count, args.wait, args.unit)
        except ValueError as err:
            log.info("Error: %s", err)
        else:
            log.info("%s successful write operations, %s errors.", result[0], result[1])

    elif args.action.lower() == "fuzz_r":
        log.info("[*] Randomly fuzz registers:")
        try:
            result = client.fuzz_registers(args.start, args.end, args.count, args.min, args.max, args.wait, args.unit)
        except ValueError as err:
            log.info("Error: %s", err)
        else:
            log.info("%s successful write operations, %s errors.", result[0], result[1])

    else:
        log.info("Action not defined.")


def print_table(result, start, count, data_type):
    mapping = {True: "ON", False: "OFF"}
    if ((data_type == "bit" and not hasattr(result, 'bits')) or
            (data_type == "register" and not hasattr(result, 'registers'))):
        log.info("Error.")
    else:
        cur = 8
        loops = 0
        log.info("")
        while(count > 0):
            if(count <= 8):
                cur = count
            if(loops == 0):
                output = "Address ["
            else:
                log.info("        "+("-"*65))
                output = "        ["
            for i in range(cur-1):
                output += " " + "{:05d}".format(start+i) + " |"
            output += " " + "{:05d}".format(start+cur-1) + " ]"
            log.info(output)
            if(data_type == "bit"):
                if(loops == 0):
                    output = "State   ["
                else:
                    output = "        ["
                for i in range(cur-1):
                    output += "  " + mapping[result.bits[i+(loops*8)]] + "  |"
                output += "  " + mapping[result.bits[cur-1+(loops*8)]] + "  ]"
            elif(data_type == "register"):
                if(loops == 0):
                    output = "Value   ["
                else:
                    output = "        ["
                for i in range(cur-1):
                    output += " " + "{:05d}".format(result.registers[i+(loops*8)]) + " |"
                output += " " + "{:05d}".format(result.registers[cur-1+(loops*8)]) + " ]"
            log.info(output)
            count -= 8
            start += 8
            loops += 1
        log.info("")


def run():
    args = create_arg_parser().parse_args()
    client = ModbusClient(log=log)
    client.connect(args.ip, args.port)
    do_action(client, args)
    client.disconnect()


if __name__ == "__main__":
    run()
