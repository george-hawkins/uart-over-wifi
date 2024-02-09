import errno
import itertools
import sys
import zlib

import serial
import time

from serial_monkey_patch import write, counter

serial.Serial.write = write

# `timeout` without a qualifier is the read timeout.
ser = serial.Serial('/dev/cu.usbserial-10', timeout=0, write_timeout=0)
print(ser.name)

buffer = b'\x42'*4096

spinner = itertools.cycle(['-', '/', '|', '\\'])
set_start = True

# TODO: use blocking write and send 512 byte lumps:
# n = 512 - (8 + 4)  # 8 for nano timestamp and 4 for zlib.adler32 CRC
# bytearray(map(random.getrandbits,(8,)*512))
# Write the 500 bytes
# Write the timestamp
# Write the CRC
# Hard loop - if diff since last write greater than x do next set of writes.
# x starts at 1ns and doubles every time you survive doing this for n seconds without
# the set of writes ever taking more than 1ms (that's plenty - a non-blocking write takes
# at worst 10us.
# Work out what n should be, try setting baud rate to 9600 and 921600 and seeing what the
# median time is between EAGAIN situations and maybe set n to 10 times the longest gap.

while True:
    if set_start:
        start_ns = time.perf_counter_ns()
        set_start = False
    counter.clear()
    count = ser.write(buffer)
    diff = time.perf_counter_ns() - start_ns
    eagain_count = counter.pop(errno.EAGAIN, None)
    if count == 0 and eagain_count == 1 and len(counter) == 0:
        sys.stdout.write('\b')
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        # print('.', end='')
    else:
        print(diff, count, eagain_count)
        set_start = True
        if len(counter) > 0:
            print(dict(counter))
            break

ser.close()

if __name__ == '__main__':
    pass
