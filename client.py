import machine

import config
import sockets
import wifi

from shared import reset, create_memory_buffer, PORT

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
        read_count = uart1.readinto(buffer)
        if read_count is not None and read_count > 0:
            write_count = sock.write(buffer[:read_count])
            if write_count != read_count:
                raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    def copy_to_uart():
        read_count = sock.readinto(buffer)
        if read_count is not None and read_count > 0:
            write_count = uart1.write(buffer[:read_count])
            if write_count != read_count:
                raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    # TODO: does the gc destroy the WiFi AP or STA?
    import gc
    print(f"BEFORE - mem_alloc: {gc.mem_alloc()}")
    print(f"BEFORE - mem_free: {gc.mem_free()}")
    gc.collect()
    print(f"AFTER - mem_alloc: {gc.mem_alloc()}")
    print(f"AFTER - mem_free: {gc.mem_free()}")

    while True:
        copy_to_socket()
        copy_to_uart()


if __name__ == "__main__":
    try:
        run(server_socket)
    except Exception as e:
        reset(e)
