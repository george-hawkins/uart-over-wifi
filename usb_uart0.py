import select
import sys

import machine
import micropython


class UsbUart0:
    _DEFAULT_BUFFER_SIZE = 2048
    _REPL_BAUD_RATE = 115200

    def __init__(self, baud_rate, buffer_size=_DEFAULT_BUFFER_SIZE):
        self._uart_output = sys.stdout.buffer
        self._buffer = bytearray(buffer_size)
        self._view = memoryview(self._buffer)
        self._uart0 = machine.UART(0, baud_rate)

        self._poller = select.poll()
        self._poller.register(sys.stdin.buffer, select.POLLIN)

        # Disable keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
        micropython.kbd_intr(-1)

    def read(self) -> memoryview:
        buffer = self._buffer
        read_byte = bytearray(1)
        offset = 0
        repeat = True
        while repeat:
            repeat = False
            for uart_input, event in self._poller.ipoll(0):
                if event != select.POLLIN:
                    raise RuntimeError(f"unexpected poll event {event}")
                else:
                    read_count = uart_input.readinto(read_byte)
                    if read_count == 1:
                        buffer[offset] = read_byte[0]
                        offset += 1
                        repeat = True
        return None if offset == 0 else self._view[:offset]

    def write(self, buffer) -> None:
        write_count = self._uart_output.write(buffer)
        expected = len(buffer)
        if write_count != expected:
            raise RuntimeError(f"only wrote {write_count} of {expected} bytes")

    def reset(self) -> None:
        # Restore normal REPL baud rate and ctrl-C behavior.
        micropython.kbd_intr(3)
        self._uart0.init(baudrate=self._REPL_BAUD_RATE)
