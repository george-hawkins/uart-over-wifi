import select
import sys
import time

import micropython

import config
import sockets
import uart0
import wifi
from shared import reset, create_memory_buffer, PORT

wifi.create_ap(config.SSID, config.PASSPHRASE)

client_socket = sockets.accept(PORT)

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


def setup_uart0():
    print(f"taking over UART0")
    time.sleep_ms(500)
    uart0.set_baud_rate(config.BAUD_RATE)
    # Disable the generation of a keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
    micropython.kbd_intr(-1)


def run(sock):
    setup_uart0()

    uart0_input = sys.stdin.buffer
    uart0_readinto = uart0_input.readinto
    uart0_write = sys.stdout.buffer.write

    poller = select.poll()
    poller.register(uart0_input, select.POLLIN)

    buffer = create_memory_buffer()

    byte_buffer = bytearray(1)

    def copy_to_socket():
        # TODO: will this starve copy_to_uart.
        for _, event in poller.ipoll(0):
            if event != select.POLLIN:
                raise RuntimeError(f"unexpected poll event {event}")
            read_count = uart0_readinto(byte_buffer)
            if read_count != 1:
                raise RuntimeError(f"failed to read byte")
            write_count = sock.write(byte_buffer)
            if write_count != 1:
                raise RuntimeError(f"failed to write byte")

    def copy_to_uart():
        read_count = sock.readinto(buffer)
        if read_count is not None and read_count > 0:
            write_count = uart0_write(buffer[:read_count])
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


failure = None

if __name__ == "__main__":
    try:
        run(client_socket)
    except Exception as e:
        reset(e)
