import time

from usb_uart0 import UsbUart0

# Give myself a chance to bail and upload a new program.
print('Press ctrl-C now to exit')
time.sleep(3)
print("Taking control of the USB UART")
time.sleep_ms(200)

usb_uart0 = UsbUart0(230400)

while True:
    try:
        buffer = usb_uart0.read()
        if buffer is not None:
            usb_uart0.write(buffer)
    except Exception as e:
        usb_uart0.reset()
        time.sleep_ms(200)
        raise e
