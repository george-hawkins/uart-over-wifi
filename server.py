import select
import socket
import sys
import time

import machine
import micropython
import network

BAUD_RATE = 57600

SSID = "iodow7he4hm5xs7l1hw5v56mf"
PASSPHRASE = "r9x08zf5dsk3qu66abp7mgbtu"

BUFFER_LEN = 2048
PORT = 2

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

ap = network.WLAN(network.AP_IF)
ap.active(True)
# Note: classic ESP32 does not support AUTH_WPA3_PSK.
ap.config(ssid=SSID, key=PASSPHRASE, security=network.AUTH_WPA2_PSK)
ap_address = ap.ifconfig()[0]
print(f"started access point with SSID {SSID} and address {ap_address}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# Port 2 was assigned by IANA but never used.
bind_address = socket.getaddrinfo('0.0.0.0', PORT, 0, socket.SOCK_STREAM)[0][-1]

server = socket.socket()
server.bind(bind_address)
server.listen(1)

# TODO: underscore here is just due to name reuse later.
client, client_address = server.accept()
client.setblocking(False)  # The default is blocking.
server.close()
print(f"client socket connected from {client_address[0]}")

print(f"taking over UART0")
time.sleep_ms(500)


def run(sock):
    machine.UART(0, baudrate=BAUD_RATE)
    uart0_input = sys.stdin.buffer
    uart0_readinto = uart0_input.readinto
    uart0_write = sys.stdout.buffer.write

    poller = select.poll()
    poller.register(uart0_input, select.POLLIN)

    # Disable the generation of a keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
    micropython.kbd_intr(-1)

    # The classic ESP32 can send at least 1424 bytes of payload per packet.
    buffer = memoryview(bytearray(BUFFER_LEN))

    byte_buffer = bytearray(1)

    def copy_to_socket():
        # TODO: will this starve copy_to_uart.
        for _, event in poller.ipoll(0):
            if event != select.POLLIN:
                raise RuntimeError(f"unexpected poll event {event}")
            read_count = uart0_readinto(byte_buffer)
            if read_count != 1:
                raise RuntimeError(f"failed to read byte")
            write_count = sock.write(byte_buffer)
            if write_count != 1:
                raise RuntimeError(f"failed to write byte")

    def copy_to_uart():
        read_count = sock.readinto(buffer)
        if read_count is not None and read_count > 0:
            write_count = uart0_write(buffer[:read_count])
            if write_count != read_count:
                raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    while True:
        copy_to_socket()
        copy_to_uart()


failure = None

if __name__ == "__main__":
    try:
        run(client)
    except Exception as e:
        failure = e  # Entry sys.print_exception(failure) in REPL to see point of failure.
        machine.UART(0, baudrate=115200)
        time.sleep_ms(500)
        micropython.kbd_intr(3)
        sys.exit(1)
        # machine.reset()
