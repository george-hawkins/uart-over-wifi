from machine import Pin
import time

LED_PIN = 8
BUTTON_PIN = 9

BUTTON_MILLIS = 200

led = Pin(LED_PIN, Pin.OUT)
led_value = 0
led_toggle_time = 0

button = Pin(BUTTON_PIN, Pin.IN)
button_value = button.value()

while True:
    now = time.ticks_ms()
    delta = time.ticks_diff(now, led_toggle_time)
    if delta >= BUTTON_MILLIS:
        led_toggle_time = now
        led.value(led_value)
        led_value = led_value ^ 1

    current_button_value = button.value()
    if current_button_value != button_value:
        print(current_button_value)
        button_value = current_button_value
