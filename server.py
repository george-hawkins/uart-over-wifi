import select
import sys
import time

import micropython

import config
import sockets
import uart0
import wifi
from shared import reset, PORT, log

log("starting")


class Runner:
    @staticmethod
    def setup_uart0():
        print(f"taking over UART0")
        time.sleep_ms(500)
        uart0.set_baud_rate(config.BAUD_RATE)
        # Disable the generation of a keyboard interrupt on receiving a 0x03 (ctrl-C) byte.
        micropython.kbd_intr(-1)

    def do_run(self, sock):
        self.setup_uart0()

        uart0_input = sys.stdin.buffer
        uart0_readinto = uart0_input.readinto
        uart0_write = sys.stdout.buffer.write

        poller = select.poll()
        poller.register(uart0_input, select.POLLIN)

        poller2 = select.poll()
        poller2.register(sock, select.POLLIN)

        # buffer = create_memory_buffer()

        buffer_len = 1024
        buffer = memoryview(bytearray(buffer_len))

        # byte_buffer = bytearray(1)

        self.offset = 0

        self.balance = 0

        def copy_to_socket():
            for _, event in poller.ipoll(0):
                if event != select.POLLIN:
                    raise RuntimeError(f"unexpected poll event {event}")
                next_offset = self.offset + 1
                read_count = uart0_readinto(buffer[self.offset:next_offset])
                if read_count != 1:
                    raise RuntimeError(f"failed to read byte")
                self.offset = next_offset
                self.balance -= 1
                if self.offset == buffer_len:
                    break
                    count = 0
                    while count < self.offset:
                        result = uart0_write(buffer[count:])
                        # result = sock.write(buffer[count:])
                        if result is not None:
                            count += result
                    self.offset = 0
            # # TODO: will this starve copy_to_uart.
            # count = 0
            # for _, event in poller.ipoll(0):
            #     if event != select.POLLIN:
            #         raise RuntimeError(f"unexpected poll event {event}")
            #
            #     start_time()
            #     read_count = uart0_readinto(byte_buffer)
            #     end_time("UART0 read")
            #     if read_count != 1:
            #         raise RuntimeError(f"failed to read byte")
            #     start_time()
            #     write_count = sock.write(byte_buffer)
            #     end_time("sock write")
            #     if write_count != 1:
            #         raise RuntimeError(f"failed to write byte")
            #     count += 1
            #     if count > 16:
            #         break

        def copy_to_uart():
            for _, event in poller2.ipoll(0):
                if event != select.POLLIN:
                    raise RuntimeError(f"unexpected poll event {event}")
                read_count = sock.readinto(buffer)
                if read_count is None:
                    raise RuntimeError(f"unexpect None")
                if read_count == 0:
                    raise RuntimeError(f"failed to read any bytes")
                self.balance += read_count
                write_count = uart0_write(buffer[:read_count])
                if write_count != read_count:
                    raise RuntimeError(f"only wrote {write_count} of {read_count} bytes.")

        # TODO: does the gc destroy the WiFi AP or STA?
        import gc
        print(f"BEFORE - mem_alloc: {gc.mem_alloc()}")
        print(f"BEFORE - mem_free: {gc.mem_free()}")
        gc.collect()
        print(f"AFTER - mem_alloc: {gc.mem_alloc()}")
        print(f"AFTER - mem_free: {gc.mem_free()}")

        log("looping")
        while True:
            #if self.balance >= 0:
                copy_to_socket()
            #if self.balance <= 0:
                copy_to_uart()

    def run(self):
        wifi.create_ap(config.SSID, config.PASSPHRASE)

        client_socket = sockets.accept(PORT)

        self.do_run(client_socket)
        # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


if __name__ == "__main__":
    try:
        Runner().run()
    except Exception as e:
        reset(e)

log("unexpected end")
