import argparse
import zlib

import serial
import time

BAUD_RATE = 9600

BLOCK_SIZE = 128

# 8N1 is 80% efficient, i.e. sending 100 bytes requires 125 bytes of bandwidth.
# See https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter#Data_framing
EFFICIENCY = 0.8

SEND_TIME_NS = ((BLOCK_SIZE * 8 * 10**9) / EFFICIENCY) / BAUD_RATE

STX = b'\x02'

# 13 = STX byte + 8 byte timestamp + 4 byte CRC.
FILLER = STX + b'#' * (BLOCK_SIZE - 13)


# Write only blocks if the underlying OS buffer is full or you attempt to write more than the
# underlying `os.write` call will accept in one go. Non-blocking writes rarely take more than
# 100us but non-blocking reads, for some reason, take more than 10ms every so often (even when
# there's nothing to read).
# If a write or read operation goes above the limits here log a (mild) warning.
WRITE_OP_NS = 10 ** 6
READ_OP_NS = 10 ** 7


def main(port, baudrate):
    def time_ns(action):
        start_ns = time.perf_counter_ns()
        result = action()
        return time.perf_counter_ns() - start_ns, result

    def write_block(now_ns):
        now_bytes = now_ns.to_bytes(8)
        crc = zlib.adler32(now_bytes)
        crc_bytes = crc.to_bytes(4)
        ser.write(FILLER)
        ser.write(now_bytes)
        ser.write(crc_bytes)

    # `timeout` without a qualifier is the read timeout.
    ser = serial.Serial(port, baudrate, timeout=0)
    print(ser.name)

    next_ns = 0

    while True:
        now_ns = time.perf_counter_ns()
        if now_ns > next_ns:
            diff_ns, _ = time_ns(lambda : write_block(now_ns))
            if diff_ns > WRITE_OP_NS:
                print(f'Write blocked for {diff_ns} ns')
            else:
                print('.', end='')
            next_ns = time.perf_counter_ns() + SEND_TIME_NS
        diff_ns, block = time_ns(lambda : ser.read(BLOCK_SIZE))
        if diff_ns > READ_OP_NS:
            print(f'Read blocked for {diff_ns} ns')
        if len(block) > 0:
            print(f'Read {len(block)} bytes')

    ser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True)
    parser.add_argument('--baudrate', type=int, required=True)
    args = parser.parse_args()
    main(args.port, args.baudrate)
