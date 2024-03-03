import select
import sys
import time
import gc

import micropython

import config
import sockets
import uart0
import wifi
import wifi_send_buffer
from shared import reset, PORT, log

log("starting")


# 7,372,800 baud is below the theoretical UART0 limit but above the maximum speed seen in practice.
# See https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/peripherals/usb.html#why-does-esp32-s2-esp32-s3-not-reach-the-maximum-usb-full-speed-12-mbps
_UART0_BAUD_RATE = 7_372_800

_SOCK_READ_BUFFER_LEN = 2048


class Runner:
    @staticmethod
    def setup_uart0(baud_rate):
        print(f"taking over UART0")
        time.sleep_ms(500)
        uart0.set_baud_rate(baud_rate)
        # Disable the generation of a keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
        micropython.kbd_intr(-1)

    @staticmethod
    def create_sock_write_buffer(baud_rate):
        write_buffer_len, delay_ns = wifi_send_buffer.get_buffer_size(baud_rate)
        delay_ms = int(delay_ns / 1_000_000)  # Nice for display.
        delay_us = int(delay_ns / 1_000)  # Nanos can't be used with `time.ticks_diff` so, switch to micros.
        print(f"Socket write buffer len: {write_buffer_len} bytes, max resulting delay before sending: {delay_ms} ms")
        write_buffer = memoryview(bytearray(write_buffer_len))
        return write_buffer, delay_us

    def do_run(self, sock):
        sock_write_buffer, send_delay_us = self.create_sock_write_buffer(config.BAUD_RATE)
        write_buffer_len = len(sock_write_buffer)

        sock_read_buffer = memoryview(bytearray(_SOCK_READ_BUFFER_LEN))

        self.setup_uart0(_UART0_BAUD_RATE)

        uart0_input = sys.stdin.buffer
        uart0_readinto = uart0_input.readinto
        uart0_write = sys.stdout.buffer.write

        poller = select.poll()
        poller.register(uart0_input, select.POLLIN)

        end_offset = 0
        next_sock_write_us = time.ticks_add(time.ticks_us(), send_delay_us)

        log("starting read/write loop")

        # Force a GC before entering the performance critical loop.
        gc.collect()

        # Important: be very careful of introducing references to global variables and calls to user functions,
        # i.e. functions not provided by the standard libraries - the time cost is surprisingly noticeable.
        while True:
            # 1. Try reading from UART0.
            if end_offset < write_buffer_len:
                for _, event in poller.ipoll(0):
                    if event != select.POLLIN:
                        raise RuntimeError(f"unexpected poll event {event}")
                    next_offset = end_offset + 1
                    read_count = uart0_readinto(sock_write_buffer[end_offset:next_offset])
                    if read_count != 1:
                        raise RuntimeError(f"failed to read byte")
                    end_offset = next_offset
                    if end_offset == write_buffer_len:
                        break  # TODO: can this `if` and the `for` be combined into a `while`.

            # 2. Try writing to the socket.
            if time.ticks_diff(next_sock_write_us, time.ticks_us()) <= 0:
                start_offset = 0
                # If `offset` is zero nothing will be written but `last_sock_write_us` is still updated.
                while start_offset < end_offset:
                    write_count = sock.write(sock_write_buffer[start_offset:end_offset])
                    if write_count is not None:
                        start_offset += write_count
                end_offset = 0
                next_sock_write_us = time.ticks_add(next_sock_write_us, send_delay_us)

            # 3. Try reading from the socket and writing to UART0.
            read_count = sock.readinto(sock_read_buffer)
            if read_count is not None:
                if read_count == 0:
                    raise RuntimeError("failed to read any bytes")
                write_count = uart0_write(sock_read_buffer[:read_count])
                if write_count != read_count:
                    raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

    def run(self):
        wifi.create_ap(config.SSID, config.PASSPHRASE)

        client_socket = sockets.accept(PORT)

        self.do_run(client_socket)


if __name__ == "__main__":
    try:
        Runner().run()
    except Exception as e:
        reset(e)

log("unexpected end")
