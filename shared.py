import config
import uart0
import micropython
import sys
import machine

# Port 2 was assigned by IANA but never used.
PORT = 2

# The classic ESP32 can send at least 1424 bytes of payload per packet.
_BUFFER_LEN = 2048

failure = None


def create_memory_buffer(size = _BUFFER_LEN):
    return memoryview(bytearray(size))


def reset(e: Exception):
    if config.DEV_MODE:
        global failure
        failure = e  # Enter sys.print_exception(failure) in REPL to see the point-of-failure.
        uart0.reset_baud_rate()
        micropython.kbd_intr(0x03)  # Restore ctrl-C behavior (only actually disabled by side using USB).
        sys.exit(1)
    else:
        machine.reset()
