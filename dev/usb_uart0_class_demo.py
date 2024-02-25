import time

from usb_uart0 import UsbUart0

BAUD_RATE = 57600


def run():
    usb_uart0 = UsbUart0(BAUD_RATE)

    while True:
        try:
            buffer = usb_uart0.read()
            if buffer is not None:
                usb_uart0.write(buffer)
        except Exception as e:
            usb_uart0.reset()
            time.sleep_ms(200)
            raise e


run()
