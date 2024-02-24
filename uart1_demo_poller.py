import select

from machine import UART

# C3
RX_PIN = 20
TX_PIN = 21
# Classic (the RXD and TXD pins on the LillyGo board are just the broken out UART0 pins).
# The WeAct classic board has the RXD and TXD pins broken out onto different columns on the right-hard side).
# RX_PIN = 3
# TX_PIN = 1
BAUD_RATE = 1843200

buffer = memoryview(bytearray(2048))

uart1 = UART(1, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, timeout=0)

poller = select.poll()
poller.register(uart1, select.POLLIN)

while True:
    for _, event in poller.ipoll(0):
        if event != select.POLLIN:
            raise RuntimeError(f"unexpected poll event {event}")
        else:
            read_count = uart1.readinto(buffer)
            write_count = uart1.write(buffer[:read_count])
            if write_count != read_count:
                raise RuntimeError(f"Only wrote {write_count} of {read_count} bytes.")
