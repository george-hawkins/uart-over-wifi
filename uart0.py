import machine
import time

_REPL_BAUD_RATE = 115200

_uart0 = None
_baud_rate = _REPL_BAUD_RATE
def set_baud_rate(new_baud_rate):
    global _baud_rate, _uart0
    if _baud_rate == new_baud_rate:
        return
    if _uart0 is None:
        _uart0 = machine.UART(0)
    _uart0.init(baudrate=new_baud_rate)
    _baud_rate = new_baud_rate
    time.sleep_ms(500)  # Wait a little while for the rate change to really take effect.


def reset_baud_rate():
    set_baud_rate(_REPL_BAUD_RATE)