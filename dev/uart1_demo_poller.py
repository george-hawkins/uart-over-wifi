import select

from machine import UART

RX_PIN = 20
TX_PIN = 21
BAUD_RATE = 230400


def run():
    buffer = memoryview(bytearray(2048))

    uart1 = UART(1, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, timeout=0)

    poller = select.poll()
    poller.register(uart1, select.POLLIN)

    def copy_to_uart():
        for _, event in poller.ipoll(0):
            if event != select.POLLIN:
                raise RuntimeError(f"unexpected poll event {event}")
            else:
                read_count = uart1.readinto(buffer)
                write_count = uart1.write(buffer[:read_count])
                if write_count != read_count:
                    raise RuntimeError(f"Only wrote {write_count} of {read_count} bytes.")

    while True:
        copy_to_uart()


run()
