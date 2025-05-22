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
