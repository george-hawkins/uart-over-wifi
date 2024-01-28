from machine import Pin
import time
import network

SSID = "iodow7he4hm5xs7l1hw5v56mf"
PASSPHRASE = "r9x08zf5dsk3qu66abp7mgbtu"

LED_PIN = 8
BUTTON_PIN = 9

BUTTON_MILLIS = 200

led = Pin(LED_PIN, Pin.OUT)
led_value = 0
led_toggle_time = 0

button = Pin(BUTTON_PIN, Pin.IN)
button_default_value = button.value()

sta = network.WLAN(network.STA_IF)
sta.active(True)

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

gateway = ""

def connect():
    while True:
        print(f"attempting to connect to SSID {SSID}")
        sta.connect(SSID, PASSPHRASE)
        if is_connected():
            address = sta.ifconfig()[0]
            global gateway
            gateway = sta.ifconfig()[2]
            print(f"connected to access point {gateway} and was assigned address {address}")
            return
        else:
            print(f"failed to connect - retrying in {_RETRY_INTERVAL} seconds")
            time.sleep(_RETRY_INTERVAL)


connect()

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

import socket

PORT = 2

s = socket.socket()

addr = socket.getaddrinfo(gateway, PORT, 0, socket.SOCK_STREAM)[0][-1]
s.connect(addr)
s.setblocking(False)  # The default is blocking.

print(f"connected socket to {gateway}")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

buffer = memoryview(bytearray(1024))

import sys

while True:
    count = s.write(buffer)
    if count is not None:
        print(".", end="")
    if button.value() != button_default_value:
        sys.exit()


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
