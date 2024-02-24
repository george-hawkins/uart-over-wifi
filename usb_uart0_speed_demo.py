import select
import sys

import micropython
from machine import UART

BAUD_RATE = 460800


def run():
    uart0 = UART(0, baudrate=BAUD_RATE)
    uart_input = sys.stdin.buffer
    uart_output = sys.stdout.buffer

    # Disable keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
    micropython.kbd_intr(-1)

    poller = select.poll()
    poller.register(uart_input, select.POLLIN)

    failure = None

    try:
        byte_buffer = bytearray(1)
        while True:
            # Letting ipoll block doesn't improve performance.
            for _, event in poller.ipoll(0):
                if event != select.POLLIN:
                    raise RuntimeError(f"unexpected poll event {event}")
                read_count = uart_input.readinto(byte_buffer)
                if read_count != 1:
                    raise RuntimeError(f"failed to read byte")
                write_count = uart_output.write(byte_buffer)
                if write_count != 1:
                    raise RuntimeError(f"failed to write byte")
    except Exception as e:
        failure = e

    micropython.kbd_intr(3)
    uart0.init(baudrate=115200)


run()
