import socket
import sys
import time

import machine
import network

SSID = "iodow7he4hm5xs7l1hw5v56mf"
PASSPHRASE = "r9x08zf5dsk3qu66abp7mgbtu"

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

sta = network.WLAN(network.STA_IF)
sta.active(True)


def connect():
    # My ESP32 takes less than 2 seconds to join, so 8s is a long timeout.
    _CONNECT_TIMEOUT = 8000
    _RETRY_INTERVAL = 5

    def is_connected():
        start = time.ticks_ms()
        while True:
            if sta.isconnected():
                return True
            diff = time.ticks_diff(time.ticks_ms(), start)
            if diff > _CONNECT_TIMEOUT:
                sta.disconnect()
                return False

    while True:
        print(f"attempting to connect to SSID {SSID}")
        sta.connect(SSID, PASSPHRASE)
        if is_connected():
            address, _, gateway, *_ = sta.ifconfig()
            print(f"connected to access point {gateway} and was assigned address {address}")
            return address, gateway
        else:
            print(f"failed to connect - retrying in {_RETRY_INTERVAL} seconds")
            time.sleep(_RETRY_INTERVAL)


_, server_address = connect()

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

PORT = 2

server_socket_address = socket.getaddrinfo(server_address, PORT, 0, socket.SOCK_STREAM)[0][-1]

server = socket.socket()
server.connect(server_socket_address)
server.setblocking(False)  # The default is blocking.

print(f"connected to server {server_address}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

BAUD_RATE = 57600

RX_PIN = 20
TX_PIN = 21

BUFFER_LEN = 2048


def run(sock):
    buffer = memoryview(bytearray(BUFFER_LEN))

    uart1 = machine.UART(1, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, timeout=0)

    # TODO: make sure no ops take too long, i.e. time and complain if they're longer than X ms.
    # TODO: I find it odd that sock.readinto and uart.readinto return None but they do.

    # TODO: make a single function and pass in uart1.readinto and sock.write or sock.readinto and uart1.write.
    def copy_to_socket():
        read_count = uart1.readinto(buffer)
        if read_count is not None and read_count > 0:
            write_count = sock.write(buffer[:read_count])
            if write_count != read_count:
                raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    def copy_to_uart():
        read_count = sock.readinto(buffer)
        if read_count is not None and read_count > 0:
            write_count = uart1.write(buffer[:read_count])
            if write_count != read_count:
                raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    while True:
        copy_to_socket()
        copy_to_uart()


failure = None

if __name__ == "__main__":
    try:
        run(server)
    except Exception as e:
        failure = e  # Entry sys.print_exception(failure) in REPL to see point of failure.
        sys.exit(1)
        # machine.reset()
