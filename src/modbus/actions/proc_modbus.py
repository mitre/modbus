import random
import time

from modbus.client import ModbusClient


@ModbusClient.action
def fuzz_coils(self, start, end, count, wait_t=0, device_id=1):
    self.log.info(
        f"Fuzz Coils -- [Addresses: {start}-{end}, Count: {count}, Wait: {wait_t}s, Device ID: {device_id}]"
    )
    success_count = 0
    error_count = 0
    if start > end:
        raise ValueError("Start address cannot be greater than end address")
    elif wait_t < 0:
        raise ValueError("Wait time cannot be less than zero")
    else:
        for _ in range(count):
            rand_addr = random.randint(start, end)
            rand_val = random.getrandbits(1)
            result = self.write_coil(rand_addr, rand_val, device_id=device_id)
            if result.isError():
                error_count += 1
            else:
                success_count += 1
            if wait_t > 0:
                time.sleep(wait_t)
        return [success_count, error_count]


@ModbusClient.action
def fuzz_registers(
    self, start, end, count, min_v=0, max_v=65535, wait_t=0, device_id=1
):
    self.log.info(
        f"Fuzz Registers -- [Addresses: {start}-{end}, Count: {count}, Min-Max: {min_v}-{max_v}, Wait: {wait_t}s, Device ID: {device_id}]"
    )
    success_count = 0
    error_count = 0
    if min_v > max_v:
        raise ValueError("Min register value cannot be greater than max register value")
    elif start > end:
        raise ValueError("Start address cannot be greater than end address")
    elif wait_t < 0:
        raise ValueError("Wait time cannot be less than zero")
    else:
        for _ in range(count):
            rand_addr = random.randint(start, end)
            rand_val = random.randint(min_v, max_v)
            result = self.write_register(rand_addr, rand_val, device_id=device_id)
            if result.isError():
                error_count += 1
            else:
                success_count += 1
            if wait_t > 0:
                time.sleep(wait_t)
        return [success_count, error_count]


def _find_highest_address(read_func, start_address, max_per_request, device_id):
    low = start_address
    high = min(65535, start_address + max_per_request - 1)

    while low <= high:
        mid = (low + high) // 2
        try:
            result = read_func(mid, count=1, slave=device_id)
            if result.isError():
                high = mid - 1
            else:
                low = mid + 1
        except Exception:
            high = mid - 1

    return high if low > start_address else -1


def _read_batch(read_func, start_address, highest_addr, device_id):
    successful_reads = []
    addr = start_address
    while addr <= highest_addr:
        remaining = highest_addr - addr + 1
        batch_size = min(remaining, 10)

        success = False
        while batch_size > 0 and not success:
            try:
                result = read_func(addr, count=batch_size, slave=device_id)
                if not result.isError():
                    if hasattr(result, "bits") and len(result.bits) == batch_size:
                        for i in range(batch_size):
                            successful_reads.append((addr + i, result.bits[i]))
                        success = True
                    elif (
                        hasattr(result, "registers")
                        and len(result.registers) == batch_size
                    ):
                        for i in range(batch_size):
                            successful_reads.append((addr + i, result.registers[i]))
                        success = True
            except Exception:
                pass

            if not success:
                batch_size = batch_size // 2

        if not success:
            for i in range(min(remaining, 10)):
                try:
                    result = read_func(addr + i, count=1, slave=device_id)
                    if not result.isError():
                        if hasattr(result, "bits") and result.bits:
                            successful_reads.append((addr + i, result.bits[0]))
                        elif hasattr(result, "registers") and result.registers:
                            successful_reads.append((addr + i, result.registers[0]))
                except Exception:
                    pass
            addr += min(remaining, 10)
        else:
            addr += batch_size

    return successful_reads


@ModbusClient.action
def scan_modbus(self, start_address=0, device_id=1):
    """
    Protocol Function
    Modbus Scan Registers
    """
    address = start_address
    self.log.info(
        f"Scanning Modbus device -- [Start Address: {address}, Device ID: {device_id}]"
    )

    func_specs = [
        (1, self.client.read_coils, 2000, "Coils", "coil"),
        ( 2, self.client.read_discrete_inputs, 2000, "Discrete Inputs", "discrete input",),
        ( 3, self.client.read_holding_registers, 125, "Holding Registers", "holding register",),
        (4, self.client.read_input_registers, 125, "Input Registers", "input register"),
    ]

    scan_results = []

    for func_code, read_func, max_per_request, name, output_name in func_specs:
        highest_addr = _find_highest_address(read_func, address, max_per_request, device_id)

        if highest_addr >= address:
            count = highest_addr - address + 1
            self.log.info(
                f"Read {name} ({func_code:02d}) -- [Address: {address}, Count: {count}, Device ID: {device_id}]"
            )

            successful_reads = _read_batch(read_func, address, highest_addr, device_id)

            if successful_reads:
                register_data = []
                for addr, value in successful_reads:
                    if func_code <= 2:
                        register_data.append(
                            f"{output_name} {addr} = {1 if value else 0}"
                        )
                    else:
                        register_data.append(f"{output_name} {addr} = {value}")

                scan_results.append(
                    {
                        "type": name,
                        "func_code": func_code,
                        "start_address": address,
                        "count": len(successful_reads),
                        "data": register_data,
                    }
                )

    return scan_results
