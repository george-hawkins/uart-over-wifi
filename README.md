UART over WiFi
==============

See [`udev-rules.md`](udev-rules.md) for `udev` rules for the WeAct Studio classic ESP32 and EP32-C3 Core boards.

Install MicroPython
-------------------

Download the latest firmware:

* For the classic ESP32 [here](https://micropython.org/download/ESP32_GENERIC/).
* For the ESP32-C3 [here](https://micropython.org/download/ESP32_GENERIC_C3/).

For the C3, the choice is easy - there's just one firmware built for this chip so, ignore the preview builds and just select the release build with the latest version number.

For the classic ESP32, there are more firmware choices. For the WeAct Studio [ESP32-D0WD-V3 Mini Core](https://www.aliexpress.com/item/1005005645111663.html) board (and for most other boards that don't have an additional external SPI RAM chip), the relevant firmware is the first one, i.e. the most generic one. When downloaded, it'll have a name something like `ESP32_GENERIC-20240105-v1.22.1.bin`.

Then install `esptool` and `monitor`:

```
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip
(env) $ pip install esptool esp-idf-monitor
```

Find the device corresponding to the connected board. On a Mac, you'd do this like so:

```
(env) $ ls /dev/cu.usbmodem*
(env) $ port=/dev/cu.usbmodem1101
```

Then erase the flash on the board and flash the firmware to the board. The following section show these steps for the classic ESP32 and the C3. The steps are almost identical for both, just the `--chip` argument and the `write_flash` address differ.

### Classic ESP32

Erase the flash on the board:

```
(env) $ esptool.py --chip esp32 --port $port erase_flash
```

Flash the firmware to the board:

```
(env) $ esptool.py --chip esp32 --port $port --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240105-v1.22.1.bin
```

### ESP32-C3

Erase the flash on the board:

```
(env) $ esptool.py --chip esp32c3 --port $port erase_flash
```

Flash the firmware to the board:

```
(env) $ esptool.py --chip esp32c3 --port $port --baud 460800 write_flash -z 0x0 ESP32_GENERIC_C3-20240105-v1.22.1.bin
```

---

Now, that the firmware is flashed to the board, you can connect to the Python REPL on the board:

```
(env) $ python -m esp_idf_monitor --port $port
--- esp-idf-monitor 1.3.4 on /dev/esp-usb-serial 115200 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
...
MicroPython v1.22.1 on 2024-01-05; ESP32C3 module with ESP32C3
Type "help()" for more information.
>>
```

As it tells you, press `ctrl-]` to quit the connection. Try entering `print('hello world')` to get started.

MicroPython stubs
-----------------

To enable PyCharm (and other IDEs) to know about the MicroPython versions of standard libraries (like `os`) and MicroPython specific libraries like `network`:

```
$ pip install micropython-esp32-stubs
```

For more information, see the MicroPython Stubs [documentation](https://micropython-stubs.readthedocs.io/en/main/24_pycharm.html).

Mpremote
--------

Over the years, many different people have created MicroPython tools that go beyond `esp_idf_monitor` and e.g. allow you to copy files to your board.

The tool that now seems to be actively maintained by the MicroPython project is [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html).

Note: there's another package on PyPi called [`mpremote2`](https://pypi.org/project/mpremote2/) but it's not mentioned in the MicroPython docs, I can't find any reference to it in the MicroPython repository and it's not released by the same maintainers as those listed for [`mpremote`](https://pypi.org/project/mpremote/).

To install it (assuming you've still got the same `venv` active as above):

```
(env) $ pip install mpremote
```

Then to connect to your board (in a similar fashion to above with `esp_idf_monitor`):

```
(env) $ mpremote repl
```

Unlike `esp_idf_monitor`, it doesn't automatically reboot the board before connecting so, it's already just waiting for input - press return to get it to print the prompt again.

Again, it's `ctrl-]` to quit.

To copy a file to the board:

```
(env) $ mpremote cp main.py :
```

See the MicroPython `mpremote` [documentation](https://docs.micropython.org/en/latest/reference/mpremote.html) for more details, e.g. the meaning of the `:` etc.

If a file is named `main.py` then the board will automatically execute it when it starts up.

If a program is running and you connect to the REPL, you'll have to press `ctrl-C` to stop the program and get to the REPL prompt.

Blinking a LED
--------------

If your board has an LED (most do except for the Seeed Xiao range of boards) then you can write a simple Python program to blink it:

```
(env) $ cat > main.py << 'EOF'
from machine import Pin
from time import sleep_ms

LED_PIN = 8

led = Pin(LED_PIN, Pin.OUT)
v = 0

while True:
    led.value(v)
    sleep_ms(200)
    v = v ^ 1
EOF
```

Change the `LED_PIN` value to match your board, the WeAct Studio ESP-C3 Core board has an LED connected to pin 8 and their classic ESP32-D0WD-V3 board uses pin 22.

And copy it to the board:

```
(env) $ mpremote cp main.py :
```

Boards typically have two buttons - one labeled `BOOT` and one labeled `RST` (reset) or `EN` (enable).

To restart the board without plugging it in and out, press the `RST` (or `EN`) button.

Or you can do:

```
(env) $ mpremote reset
```

Multiple boards
---------------

The above commands are all automatically searching for and operating against the first board they find.

If you've got multiple boards connected then you have to explicitly specify which board to use.

E.g. I've got boards connected on `/dev/ttyACM0` and `/dev/ttyUSB0`. To do an `ls` on a specific board:

```
(env) $ mpremote connect port:/dev/ttyACM0 ls
```

The `connect port:/dev/ttyACM0` tells it which port to use. The `mpremote` documentation lists predefined shortcuts for the commonly used ports on Windows and Linux (and covers how to define additional shortcuts, e.g. if you're using a Mac).

So you can replace e.g. `connect /dev/ttyUSB0` with the shortcut `u0`:

```
(env) $ mpremote u0 ls
```

Intead of using shortcuts, I just used shell variables like so and associated a more obvious name with the two boards I had connected (a classic ESP32 board and a C3 board):

```
(env) $ classic='connect port:/dev/ch340-usb-serial'
(env) $ c3='connect /dev/esp-usb-serial'
```

Then I created [`led-and-button-classic.py`](led-and-button-classic.py) and [`led-and-button-c3.py`](led-and-button-c3.py) and could copy them to the appropriate board, reset the board and connect to its REPL all in one go.

Like so for the classic ESP32 board:

```
(env) $ mpremote $classic cp led-and-button-classic.py :main.py + reset + repl
```

And for the C3 board:

```
(env) $ mpremote $c3 cp led-and-button-c3.py :main.py + reset + repl
```

If you look at [`led-and-button-c3.py`](led-and-button-c3.py), you'll see `BUTTON_PIN = 9` - the `BOOT` button on the board is connected to pin 9 and once the board has started, the `BOOT` button can be used as a normal button (it only does something special if held down while the board is starting up).

So, if `led-and-button-c3.py` is running and you're connected to the board, it'll print out the current value (1 or 0) of the `BOOT` button each time you press or release it.

Client and server
-----------------

Server:

```
$ classic='connect port:/dev/ch340-usb-serial'
$ mpremote $classic cp server-classic.py :main.py + reset + repl
```

Client:

```
$ c3='connect /dev/esp-usb-serial'
$ mpremote $c3 cp client-c3.py :main.py + reset + repl
```

ESP classic read speed
----------------------

The `cl.readinto` operation (where `cl` is the first element of the tuple returned by the socket `accept` call) is quite slow - reading 1024 bytes takes between 1.8 and 2.2ms. Trying to read when there's nothing there takes 0.6ms.

If you can handle 8 * 1024 bits per 2.2ms that's still a respectable 3.7m baud. However, our application has to do various other things in addition to just reading.

Theoretical maximum baud rate
-----------------------------

ArduPilot notes 921600 as a reliable upper limit for STM32 boards - see [`AP_SerialManager.cpp:724`](https://github.com/ArduPilot/ardupilot/blob/2cb177e/libraries/AP_SerialManager/AP_SerialManager.cpp#L724).

For comparison, Betaflight doesn't support above 115200 for GPS or telemetry (see [`ports.js:70`](https://github.com/betaflight/betaflight-configurator/blob/40c243f/src/js/tabs/ports.js#L70) in the Betaflight Configurator) but does support up to 1,000,000 baud for MSP and 2,470,000 for the blackbox,

Select.poll
-----------

At the moment I'm unconvinced there's anything to be gained wusing the `select.poll` vs just a hard loop of non-blocking reads.

For reference, here's the initial `poll` implementation that I was using:

```
poller = select.poll()
poller.register(cl, select.POLLIN | select.POLLERR | select.POLLHUP)

while True:
    for (s, event) in poller.ipoll(0):
        if event != select.POLLIN:
            # TODO: raise exception.
            print(f"got unexprected event {event}")
        elif s != cl:
            # TODO: raise exception.
            print(f"got unexprected object {s}")
        else:
            count = cl.readinto(buffer)
            if count is not None:
                print(count)
```

Effective speed
---------------

Maximum speeds reading and echoing back data.

UART0 over USB:

* C3: ~300 kbps (with baud rate set to 460,800)
* Classic (with CH340K serial-to-USB chip): ~114 kbps (with baud rate set to 115,200) 

UART1 via CP2102N:

* C3: ~1.75 mbps (with baud rate set to 1,843,200)
* Classic: ditto

Reading a byte at a time
------------------------

Reading and writing via a `machine.UART` instance, where non-blocking reads of as many bytes as are currently available in a single `readinto` call, is extremely efficient and one can effectively consume all available bandwidth up to 1,843,200 baud (which is effectively the top speed of my CP2102N based [serial to USB converter](https://www.adafruit.com/product/5335)).

But with UART0, one has to work through the blocking `sys.stdin` and this forces us into polling and reading at most one byte at a time. On a C3, a hard poll-read-write loop of a byte-at-a-time maxes out ~300kbps.

It's the performance of this loop rather than the underlying read and write operations that becomes the limiting factor.

The MicroPython documentation contains a [maximizing speed](https://docs.micropython.org/en/latest/reference/speed_python.html) page.

I tried all the suggestions - things like caching object references didn't noticeably affect speed (maybe the interpreter has been improved since this page was written) and the most interesting looking thing, the `@micropython.viper` decorator, isn't supported for C3 - as of Feb 24th, 2024, [`ports/esp32/mpconfigport.h`](https://github.com/micropython/micropython/blob/master/ports/esp32/mpconfigport.h) only supports emitting machine instructions for the Xtensa ESP32 chips:

```
#if !CONFIG_IDF_TARGET_ESP32C3
#define MICROPY_EMIT_XTENSAWIN              (1)
#endif
```

Surprisingly, the biggest gain was achieved on the basis of the advice in the [_Variables_ section](https://docs.micropython.org/en/latest/develop/optimizations.html#variables) of the _Optimizations_ page. In my tests, I'd created various variables in the global scope. Simply shifting everything into a function and calling that increased the effective throughput from ~200kbps to ~300kbps.

I.e. I started with variables like `poller` existing in the global scope:

```
poller = select.poll()

while True:
    for _, event in poller.ipoll():
        ...
```

Simply moving things into a function greatly increases performance:

```
def run()
    poller = select.poll()

    while True:
        for _, event in poller.ipoll():
            ...
            
run()
```

I suspect that a better approach than optimization like this would be an update to MicroPython to enable non-blocking reads on `sys.stdin` so that `readinto` can be used to read more than a single byte as one is currently constrained to do.