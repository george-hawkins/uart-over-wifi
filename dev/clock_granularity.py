import time


# While there is a time_ns(), there is no ticks_ns(). time_ns() comes with the warning that it may involve a heap
# allocation due to the size of the integer used to store such values. ticks_cpu() is the finest resolution but
# the duration of a CPU tick is device specific (and doesn't have to be tied to e.g. the CPU's clock frequency).
def smallest_ticks_us_increment_v1():
    min_diff = 1_000_000_000
    prev = time.ticks_us()
    while True:
        now = time.ticks_us()
        diff = time.ticks_diff(now, prev)
        if diff != 0 and diff < min_diff:
            min_diff = diff
            print(f"Diff: {diff} us")
        prev = now


def smallest_ticks_us_increment_v2():
    min_diff = -1_000_000_000
    while True:
        # The order in which the arguments are evaluated means we get negative values.
        diff = time.ticks_diff(time.ticks_us(), time.ticks_us())
        if diff != 0 and diff > min_diff:
            min_diff = diff
            print(f"Diff: {-diff} us")


# The difference between smallest_ticks_us_increment_v1() and smallest_ticks_us_increment_v2() _seems_ to indicate that
# even when measuring as coarsely as us ticks, the cost of just maintaining the variables involved becomes noticeable.
smallest_ticks_us_increment_v2()
