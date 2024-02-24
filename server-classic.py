from machine import Pin
import network

# You need a 25 digit base 36 value to encode a UUID.
# Generate ten of these with https://www.random.org/strings/?num=10&len=25&digits=on&loweralpha=on&unique=on&format=html&rnd=new
# And choose any two, one as the ESSID and one as the passphrase, and update the ESSID and PASSPHRASE values in both server.py and client.py
SSID = "iodow7he4hm5xs7l1hw5v56mf"
PASSPHRASE = "r9x08zf5dsk3qu66abp7mgbtu"

LED_PIN = 22
BUTTON_PIN = 0

BUTTON_MILLIS = 200

led = Pin(LED_PIN, Pin.OUT)
led_value = 0
led_toggle_time = 0

button = Pin(BUTTON_PIN, Pin.IN)
button_default_value = button.value()

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

class BasicLogger:
    def __init__(self):
        self._need_newline = False

    def print_char(self, c):
        print(c, end='')
        self._need_newline = True

    def print_line(self, line):
        if self._need_newline:
            print()
            self._need_newline = False
        print(line)


logger = BasicLogger()

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

ap = network.WLAN(network.AP_IF)
ap.active(True)
# Note: classic ESP32 does not support AUTH_WPA3_PSK.
ap.config(ssid=SSID, key=PASSPHRASE, security=network.AUTH_WPA2_PSK)
address = ap.ifconfig()[0]
logger.print_line(f"started access point with SSID {SSID} and address {address}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# Port 2 was assigned by IANA but never used.
PORT = 2

import socket
addr = socket.getaddrinfo('0.0.0.0', PORT, 0, socket.SOCK_STREAM)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

# TODO: `address`, `addr` and `a` - all a bit overlapping!
#cl, a = s.accept()
#cl.setblocking(False)  # The default is blocking.
#s.close()
#logger.print_line(f"client socket connected from {a[0]}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# The classic ESP32 can send at least 1424 bytes of payload per packet.
buffer = memoryview(bytearray(1024))

import select
import sys

# Classic
RX_PIN = 3
TX_PIN = 1
#RX_PIN = 40
#TX_PIN = 41
BAUD_RATE = 9600

from machine import UART

uart0 = None

# TODO: maybe toggle LED on every successful write - does it flicker or just look dim?
while True:
    # before = time.ticks_us()
    # # Do something...
    # after = time.ticks_us()
    # delta = time.ticks_diff(after, before)
    # logger.print_line(delta, count)
    # if uart0 is not None:
    #     read_count = uart1.readinto(buffer)
    #     if read_count is not None and read_count > 0:
    #         write_count = s.write(buffer[:read_count])
    #         if write_count != read_count:
    #             logger.print_line(f"Only wrote {write_count} of {read_count} bytes.")
    #         else:
    #             logger.print_char('+')

    #     read_count = cl.readinto(buffer)
    #     if read_count is not None and read_count > 0:
    #         write_count = uart1.write(buffer[:read_count])
    #         if write_count != read_count:
    #             logger.print_line(f"Only wrote {write_count} of {read_count} bytes.")
    #         else:
    #             logger.print_char('-')

    if button.value() != button_default_value:
        if uart0 is None:
            print("A")
            #os.dupterm(None, 0)
            uart0 = UART(1, baudrate=BAUD_RATE, tx=41, rx=40, timeout=0)
            #print("B")
        else:
            #print("C")
            #import os
            #uart0 = None
            #os.dupterm(UART(0, 115200, tx=1, rx=3), 0)
            #print("D")

            # TODO: restore UART (only server side needs this - ensure works as expected for both classic and C3 USB setups).
            sys.reset()

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# HERE: don't implement smart recovery - just reset the device on any error.
#  Just wrap whatever __main__ bit calls in an all encompassing exception catcher.

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

while True:
    now = time.ticks_ms()
    delta = time.ticks_diff(now, led_toggle_time)
    if delta >= BUTTON_MILLIS:
        led_toggle_time = now
        led.value(led_value)
        led_value = led_value ^ 1

    current_button_value = button.value()
    if current_button_value != button_default_value:
        logger.print_line(current_button_value)
        button_default_value = current_button_value
