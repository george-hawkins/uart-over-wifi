from machine import Pin
import time
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

ap = network.WLAN(network.AP_IF)
ap.active(True)
# Note: classic ESP32 does not support AUTH_WPA3_PSK.
ap.config(ssid=SSID, key=PASSPHRASE, security=network.AUTH_WPA2_PSK)
address = ap.ifconfig()[0]
print(f"started access point with SSID {SSID} and address {address}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# Port 2 was assigned but never used.
PORT = 2

import socket
addr = socket.getaddrinfo('0.0.0.0', PORT, 0, socket.SOCK_STREAM)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

# TODO: `address`, `addr` and `a` - all a bit overlapping!
cl, a = s.accept()
cl.setblocking(False)  # The default is blocking.
s.close()
print(f"client socket connected from {a[0]}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# The classic ESP32 can send at least 1424 bytes of payload per packet.
buffer = memoryview(bytearray(1024))

import select
import sys

poller = select.poll()
poller.register(cl, select.POLLIN | select.POLLERR | select.POLLHUP)

# TODO: is the poller worth it - just do a hard loop of non-blocking reads.
# TODO: maybe toggle LED on every successful write - does it flicker or just look dim?
while True:
    # TODO: `s` clashes with `s` above.
    for (s, event) in poller.ipoll(0):
        if event != select.POLLIN:
            # TODO: raise exception.
            print(f"got unexprected event {event}")
        elif s != cl:
            # TODO: raise exception.
            print(f"got unexprected object {s}")
        else:
            count = cl.readinto(buffer)
            if count is not None:
                print(".", end="")
    if button.value() != button_default_value:
        # TODO: restore UART (only server side needs this - ensure works as expected for both classic and C3 USB setups).
        sys.exit()

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
        print(current_button_value)
        button_default_value = current_button_value
