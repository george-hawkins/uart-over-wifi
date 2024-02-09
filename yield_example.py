def foo():
    for i in range(0, 16):
        print(f"> {i}")
        j = yield i
        print(f"> {j}")
        yield j


print(f"* 1")
gen = foo()
print(f"* 2")


def s(c):
    print(f"* {c}")
    r = gen.send(c)
    print(f"* {r}")


print(f"* 3")

# `next(gen)` is the same as `gen.send(None)`.
# We haven't even reached the first yield yet.
# It's only on `send(None)` that the generator does anything at all.
# The for-loop runs and we get to the first yield, it returns 1 to
# us but blocks from the generator's perspective.
# It's only a _subsequent_ `send` that unblocks it and it's _that_ send's value that it returns.
p = next(gen)
print(p)
#s(None)

s('B')
s('C')
s('D')
s('E')
s('F')


if __name__ == '__main__':
    pass
