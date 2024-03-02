import machine

import config
import sockets
import wifi

from shared import reset, create_memory_buffer, PORT, start_time, end_time, log

log("starting")

_, server_address = wifi.connect_to_ap(config.SSID, config.PASSPHRASE)

server_socket = sockets.connect(server_address, PORT)

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


def run(sock):
    buffer = create_memory_buffer()

    uart1 = machine.UART(1, baudrate=config.BAUD_RATE, tx=config.TX_PIN, rx=config.RX_PIN, timeout=0)

    # TODO: make sure no ops take too long, i.e. time and complain if they're longer than X ms.
    # TODO: I find it odd that sock.readinto and uart.readinto return None but they do.

    # TODO: make a single function and pass in uart1.readinto and sock.write or sock.readinto and uart1.write.
    def copy_to_socket():
        start_time()
        read_count = uart1.readinto(buffer)
        end_time("UART1 read")
        if read_count is None:
            return
        start_time()
        # TODO: this was the only one seen to fail to write fully in practice but the server.py _socket_ should be the same.
        count = 0
        while count < read_count:
            result = sock.write(buffer[count:read_count])
            if result is not None:
                count += result
        end_time("sock write")

    def copy_to_uart():
        start_time()
        read_count = sock.readinto(buffer)
        end_time("sock read")
        if read_count is None:
            return
        start_time()
        write_count = uart1.write(buffer[:read_count])
        end_time("UART1 write")
        if write_count != read_count:
            raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    # TODO: does the gc destroy the WiFi AP or STA?
    import gc
    print(f"BEFORE - mem_alloc: {gc.mem_alloc()}")
    print(f"BEFORE - mem_free: {gc.mem_free()}")
    gc.collect()
    print(f"AFTER - mem_alloc: {gc.mem_alloc()}")
    print(f"AFTER - mem_free: {gc.mem_free()}")

    log("looping")
    while True:
        copy_to_socket()
        copy_to_uart()


if __name__ == "__main__":
    try:
        run(server_socket)
    except Exception as e:
        reset(e)

log("unexpected end")
