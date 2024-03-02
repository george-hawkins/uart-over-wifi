import argparse
import statistics
import time
import zlib

import serial

TIMESTAMP_BYTE_COUNT = 8
CRC_BYTE_COUNT = 4

BLOCK_SIZE = 128

FILLER_BYTE = 0x23  # The '#' character.
FILLER_BYTE_COUNT = BLOCK_SIZE - (1 + TIMESTAMP_BYTE_COUNT + CRC_BYTE_COUNT)  # Additional 1 is the STX byte.

STX = 0x02

FILLER = bytes([STX]) + bytes([FILLER_BYTE]) * FILLER_BYTE_COUNT

# 8N1 is 80% efficient, i.e. sending 100 bytes requires 125 bytes of bandwidth.
# See https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter#Data_framing
EFFICIENCY = 0.8

# Write only blocks if the underlying OS buffer is full, or you attempt to write more than the
# underlying `os.write` call will accept in one go. Non-blocking writes rarely take more than
# 100us but non-blocking reads, for some reason, take more than 10ms every so often (even when
# there's nothing to read).
# If a write or read operation goes above the limits here log a (mild) warning.
SLOW_OP_NS = 2 * 10 ** 7

NO_READ_WARNING_S = 4


class BasicLogger:
    def __init__(self):
        self._need_newline = False

    def print_char(self, c):
        print(c, end='', flush=True)
        self._need_newline = True

    def print_line(self, line):
        if self._need_newline:
            print()
            self._need_newline = False
        print(line)


logger = BasicLogger()


class TimeDelta:
    _MICRO = 10 ** 3
    _MILLI = 10 ** 6
    _SECOND = 10 ** 9

    @classmethod
    def to_str(cls, diff_ns):
        if diff_ns > cls._SECOND:
            return f"{int(diff_ns / cls._SECOND)} s"
        elif diff_ns > cls._MILLI:
            return f"{int(diff_ns / cls._MILLI)} ms"
        elif diff_ns > cls._MICRO:
            return f"{int(diff_ns / cls._MICRO)} us"
        else:
            return f"{diff_ns} ns"


class ReadStats:
    _DURATION_NS = 10 * (10 ** 9)

    _start_ns: int
    _discarded: int
    _desync_count: int
    _bad_crc_count: int
    _latencies: list[int]

    def __init__(self, baud_rate):
        self._reset()
        self._blocks_per_second = int(baud_rate / (BLOCK_SIZE * 8 / EFFICIENCY))

    def _reset(self):
        self._start_ns = time.perf_counter_ns()
        self._discarded = 0
        self._desync_count = 0
        self._bad_crc_count = 0
        self._latencies = []

    def inc_discarded(self):
        logger.print_char('?')
        self._discarded += 1

    def inc_desync(self):
        logger.print_line('Desynced')
        self._desync_count += 1

    def inc_bad_crc_count(self):
        logger.print_line('Bad CRC')
        self._bad_crc_count += 1

    def inc_blocks(self, latency):
        self._latencies.append(latency)
        if len(self._latencies) % self._blocks_per_second == 0:
            logger.print_char('.')
        diff_ns = time.perf_counter_ns() - self._start_ns
        if diff_ns >= self._DURATION_NS:
            block_count = len(self._latencies)
            bits = block_count * BLOCK_SIZE * 8 / EFFICIENCY
            bits_per_second = bits * (10 ** 9) / diff_ns
            logger.print_line(f'Effective speed: {int(bits_per_second):,} bps')

            self._latencies.sort()
            min_latency = TimeDelta.to_str(self._latencies[0])
            max_latency = TimeDelta.to_str(self._latencies[-1])
            median_latency = TimeDelta.to_str(statistics.median(self._latencies))
            logger.print_line(f'Blocks received: {block_count}')
            logger.print_line(f'Latencies: min={min_latency}, median={median_latency}, max={max_latency}')

            logger.print_line(f'Bad CRCs: {self._bad_crc_count}')
            logger.print_line(f'Desynced: {self._desync_count}')
            logger.print_line(f'Discarded: {self._discarded}')
            self._reset()


class Reader:
    _started: bool
    _filler_count: int
    _timestamp_offset: int
    _crc_offset: int

    def __init__(self, baud_rate):
        self._timestamp = bytearray(TIMESTAMP_BYTE_COUNT)
        self._crc = bytearray(CRC_BYTE_COUNT)
        self._stats = ReadStats(baud_rate)
        self._reset()

    def _reset(self):
        self._started = False
        self._filler_count = 0
        self._timestamp_offset = 0
        self._crc_offset = 0

    def consume(self, b):
        if not self._started:
            if b == STX:
                self._started = True
            else:
                self._stats.inc_discarded()
        elif self._filler_count < FILLER_BYTE_COUNT:
            if b == FILLER_BYTE:
                self._filler_count += 1
            else:
                self._stats.inc_desync()
                self._started = False
        elif self._timestamp_offset < TIMESTAMP_BYTE_COUNT:
            self._timestamp[self._timestamp_offset] = b
            self._timestamp_offset += 1
        elif self._crc_offset < CRC_BYTE_COUNT:
            self._crc[self._crc_offset] = b
            self._crc_offset += 1
            if self._crc_offset == CRC_BYTE_COUNT:
                calculated_crc = zlib.adler32(self._timestamp)
                received_crc = int.from_bytes(self._crc, 'big')
                if calculated_crc == received_crc:
                    received_timestamp = int.from_bytes(self._timestamp, 'big')
                    diff_ns = time.perf_counter_ns() - received_timestamp
                    self._stats.inc_blocks(diff_ns)
                else:
                    self._stats.inc_bad_crc_count()
                self._reset()


def time_ns(action):
    start_ns = time.perf_counter_ns()
    result = action()
    return time.perf_counter_ns() - start_ns, result


class SerialTester:
    def __init__(self, port, baud_rate):
        self._serial = serial.Serial(port, baud_rate, timeout=0)  # `timeout` without a qualifier is the read timeout.
        self._baud_rate = baud_rate

    def write_block(self, now_ns):
        now_bytes = now_ns.to_bytes(TIMESTAMP_BYTE_COUNT, 'big')  # In Python 3.11, `byteorder` defaults to big.
        crc = zlib.adler32(now_bytes)
        crc_bytes = crc.to_bytes(CRC_BYTE_COUNT, 'big')
        self._serial.write(FILLER)
        self._serial.write(now_bytes)
        self._serial.write(crc_bytes)

    def run(self):
        try:
            reader = Reader(self._baud_rate)
            send_time_ns = ((BLOCK_SIZE * 8 * 10 ** 9) / EFFICIENCY) / self._baud_rate
            # send_time_ns *= 2
            send_time_ns = 0
            next_ns = 0
            last_read = time.perf_counter()
            no_read_factor = 1

            while True:
                now_ns = time.perf_counter_ns()
                if now_ns > next_ns:
                    diff_ns, _ = time_ns(lambda: self.write_block(now_ns))
                    if diff_ns > SLOW_OP_NS:
                        logger.print_line(f'Write blocked for {TimeDelta.to_str(diff_ns)}')
                    next_ns = time.perf_counter_ns() + send_time_ns
                diff_ns, block = time_ns(lambda: self._serial.read(BLOCK_SIZE))
                if diff_ns > SLOW_OP_NS:
                    logger.print_line(f'Read blocked for {TimeDelta.to_str(diff_ns)}')
                if len(block) > 0:
                    last_read = time.perf_counter()
                    no_read_factor = 1
                    for b in block:
                        reader.consume(b)
                else:
                    diff = time.perf_counter() - last_read
                    if diff > (NO_READ_WARNING_S * no_read_factor):
                        logger.print_line(f'No bytes received in the last {int(diff)} seconds')
                        no_read_factor += 1
        except Exception as e:
            self._serial.close()
            raise e


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True)
    parser.add_argument('--baud-rate', type=int, required=True)
    args = parser.parse_args()

    tester = SerialTester(args.port, args.baud_rate)
    tester.run()
