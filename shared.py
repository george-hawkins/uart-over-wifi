import time

import config
import uart0
import micropython
import sys
import machine

# Port 2 was assigned by IANA but never used.
PORT = 2

# The classic ESP32 can send at least 1424 bytes of payload per packet.
_BUFFER_LEN = 2048

# Enter the following in the REPL to see the point-of-failure.
# >>> import sys
# >>> from shared import failure
# >>> sys.print_exception(failure)
failure = None


def create_memory_buffer(size=_BUFFER_LEN):
    return memoryview(bytearray(size))


def log(s):
    with open('log.txt', 'a') as f:
        f.write(str(time.time()))
        f.write(' ')
        f.write(s)
        f.write('\n')


def reset(e: Exception):
    if config.DEV_MODE:
        e_str = None if e is None else str(e)
        log(f"reset exception {e_str}")
        global failure
        failure = e  # See above for how to print from REPL.
        uart0.reset_baud_rate()
        micropython.kbd_intr(0x03)  # Restore ctrl-C behavior (only actually disabled by side using USB).
        raise e
    else:
        machine.reset()


_start = time.ticks_ms()


def start_time():
    global _start
    _start = time.ticks_ms()


def end_time(op):
    diff = time.ticks_diff(time.ticks_ms(), _start)
    if diff > 500:
        log(f"{op} took {diff} ms")
