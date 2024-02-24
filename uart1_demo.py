from machine import UART

# C3
RX_PIN = 20
TX_PIN = 21
BAUD_RATE = 1843200

buffer = memoryview(bytearray(2048))

uart1 = UART(1, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, timeout=0)

while True:
    read_count = uart1.readinto(buffer)
    if read_count is not None and read_count > 0:
        write_count = uart1.write(buffer[:read_count])
        if write_count != read_count:
            raise RuntimeError(f"Only wrote {write_count} of {read_count} bytes.")
