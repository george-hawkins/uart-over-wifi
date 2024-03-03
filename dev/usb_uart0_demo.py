import select
import sys

import micropython
from machine import UART

BAUD_RATE = 230400


def run():
    UART(0, baudrate=BAUD_RATE)
    uart_input = sys.stdin.buffer
    uart_output = sys.stdout.buffer

    # Disable keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
    micropython.kbd_intr(-1)

    poller = select.poll()
    poller.register(uart_input, select.POLLIN)

    byte_buffer = bytearray(1)

    def copy_to_uart():
        for _, _ in poller.ipoll(0):
            uart_input.readinto(byte_buffer)
            uart_output.write(byte_buffer)

    while True:
        copy_to_uart()


run()
