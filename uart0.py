import machine

import config

_REPL_BAUD_RATE = 115200

_uart0 = None
_baud_rate = _REPL_BAUD_RATE


def set_baud_rate(new_baud_rate):
    if not config.NATIVE_USB:
        global _baud_rate, _uart0
        if _baud_rate == new_baud_rate:
            return
        if _uart0 is None:
            print(f"1. Setting baud rate to {new_baud_rate}")
            _uart0 = machine.UART(0, baudrate=new_baud_rate)
        else:
            print(f"2. Setting baud rate to {new_baud_rate}")
            _uart0.init(baudrate=new_baud_rate)
        _baud_rate = new_baud_rate


def reset_baud_rate():
    set_baud_rate(_REPL_BAUD_RATE)