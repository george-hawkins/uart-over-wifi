import select
import sys
import time

import micropython
from machine import UART

# https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/peripherals/usb.html#why-does-esp32-s2-esp32-s3-not-reach-the-maximum-usb-full-speed-12-mbps
# So, 7372800 would be above the actual limit but below the theoretical one.
# If I take the breaks off on the serial-tester will it limit itself to not sending faster than 115kbps?
# NO!!! But maybe one could achieve that effect my throttling ones reads from the host.
BAUD_RATE = 115200


# Give myself a chance to bail and upload a new program.
print('Press ctrl-C now to exit')
time.sleep(3)
print("Taking control of the USB UART")
time.sleep_ms(200)


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
