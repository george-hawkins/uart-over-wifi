_EFFICIENCY = 0.8  # 8N1 is 80% efficient.

# 100 ms is the typical delay introduced by Nagle's algorithm. So, let's (fairly arbitrarily)
# use that as a measure of the maximum acceptable delay in this kind of context.
_MAX_DELAY_NS = 100 * 10 ** 6

# It's hard to get a definite value of the optimal payload size for TCP/IP over Wi-Fi.
# The 802.11 MTU is 2304 which, depending on various factors, should leave 2236 for payload.
# It would be nice to see actual Wireshark dumps of ESP32 traffic to see how encryption etc. affects things.
_MAX_BUFFER_SIZE = 2048


def _nanos_for_bytes(byte_count, baud_rate):
    transmit_time_ns = ((byte_count * 8 * 10 ** 9) / _EFFICIENCY) / baud_rate
    return transmit_time_ns


def _bytes_for_nanos(transmit_time_ns, baud_rate):
    byte_count = transmit_time_ns * (_EFFICIENCY * baud_rate) / (8 * 10 ** 9)
    return byte_count


def get_buffer_size(baud_rate):
    byte_count = _bytes_for_nanos(_MAX_DELAY_NS, baud_rate)
    byte_count = min(byte_count, _MAX_BUFFER_SIZE)
    delay_ns = _nanos_for_bytes(byte_count, baud_rate)
    return int(byte_count), int(delay_ns)


if __name__ == "__main__":
    def show(baud_rate):
        count, nanos = get_buffer_size(baud_rate)
        millis = int(nanos / 10 ** 6)
        print(f"{baud_rate:,} baud: buffer-size = {count} bytes, delay = {millis} ms")

    show(9_600)  # The classic modern default minimum rate.
    show(57_600)  # Default rate for SiK radios.
    show(115_200)  # Max rate for GPS and telemetry in Betaflight.
    show(230_400)  # 300 bps is the max I've achieved on UART0 using MicroPython - so, 230_400 is achievable.
    show(460_800)  # And 460_800 is not quite achievable.
    show(921_600)  # The max rate noted for reliable STM32 UART performance in ArduPilot code.
    show(1_843_200)  # The max effective rate for my CP2102N serial-to-UART converter.
