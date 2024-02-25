import time
import machine
from machine import Pin

LED_PIN = 8

def run():
    led = Pin(LED_PIN, Pin.OUT)
    led_value = led.value

    timer0 = machine.Timer(0)

    def toggle(_: machine.Timer):
        led_value(led_value() ^ 1)

    while True:
        timer0.init(period=500, callback=toggle)
        time.sleep(5)
        timer0.deinit()
        time.sleep(5)

run()

