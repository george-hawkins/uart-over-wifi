<img width="492" height="160" src="images/logo.svg" alt="logo">

UART over Wi-Fi
===============

UART over Wi-Fi for less than US$10 without any configuration and without any dependency on an existing Wi-Fi network or smartphone hotspot with an easily achievable open-air range of X m.

| Normal wired UART connection | The same connection but wireless |
|------------------------------|----------------------------------|
| ![wired-connection](images/wired-connection.jpg) | ![wireless-connection](images/wireless-connection.jpg) |

TODO: include `wireless-connection.jpg` once you have USB-C power adapters. Use two of the Super Mini boards, a Dupont connector and the Pi Pico on a breadboard. And update `wired-connection.jpg` to match this setup (i.e. get rid of the Uno).

There's no magic to this project, it just relies on the fact that you can now get incredibly cheap [ESP32](https://en.wikipedia.org/wiki/ESP32) based boards - combine two of them and they can create their own private Wi-Fi network, discover each other and then pass the UART data back and forward over Wi-Fi.

---

See the [`dev.md`](docs/dev.md) for development notes and [`notes.md`](docs/notes.md) for notes that didn't otherwise fit elsewhere.

Boards
------

There are no end of small cheap ESP32 boards. I've used the C3 variant of the ESP32 almost exclusively and I suggest using an S3 or C3 board as the S and C range of chips have builtin USB support (whereas the original ESP32 requires an external third-party USB-to-serial chip).

You'll need two boards - one for each side of the UART connection. Here are the boards, I recommend:

* [WeAct ESP32-C3 Core board](https://www.aliexpress.com/item/1005004960064227.html)
* [Seeed Xiao ESP32-C3 board](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html)
* [Seeed Xiao ESP32-S3 board](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html)
* [Waveshare ESP32-C3 Mini board](https://www.waveshare.com/esp32-c3-zero.htm)
* [Adafruit QT Py ESP32-C3 board](https://www.adafruit.com/product/5405)
* [Sparkfun Pro Micro ESP32-C3 board](https://www.sparkfun.com/products/23484)

The Seeed Xiao is the only one where I suggest an S3 board as an alternative to the C3 variant - the S3 and C3 boards are almost identical (other than the MCU) but the C3 is the only one of the above boards that does not a user controllable LED. This may seem a minor point but I find having a builtin LED can be very useful signalling the state of the board (e.g. flashing the LED while the board is going through the setup phase of establishing a connection).

The Adafruit and Waveshare boards have a neo-pixel (a WS2812 on the Waveshare board and a WS2812B on the Adafruit board) while the others (except the Xiao C3) have a standard classic SMD LED.

There are other nice mini boards but I've excluded boards, like the lovely [TinyS3](https://esp32s3.com/tinys3.html) because at US$20, they're significantly more expensive than the boards listed above. [Lilygo](https://www.lilygo.cc/collections/all) is another provider of cheap ESP32 boards - however, their boards tend to be combined with someother device (most commonly an LCD) and all their plain ESP32 boards seem to be a slightly larger form-factor than the ones listed above.

There are no end of no-brand ESP32 boards on AliExpress. However, I suggest you get a board from a clear source like the ones above. There is one no-brand board that I will mention as it appears everywhere - the Super Mini. I've bought these from several different AliExpress stores and they seem to all work fine - for a small section about them and links to the stores, see [`notes.md`](docs/notes.md).

### Antenna

The Adafruit and Waveshare boards above come with a small ceramic chip antenna. The WeAct and Sparkfun boards come with an [inverted-F PCB antenna](https://en.wikipedia.org/wiki/Inverted-F_antenna).

The Xiao boards are interesting in that they come with a u.FL antenna connector and a patch antenna. The patch antenna probably isn't significantly better than the other antenna types but the u.FL connector means you choose to use another antenna. Seeed sell a suitable larger [whip-style antenna](https://www.seeedstudio.com/2-4GHz-2-81dBi-Antenna-for-XIAO-ESP32C3-p-5475.html) and many other manufacturers sell antennas in all shapes and sizes for 2.4GHz Wi-Fi with a u.FL connector.

Note: the u.FL connector is one of my least favorite connectors - it's very fiddly and, worse, it's extremely easy to tear these connectors off their boards when trying to remove an antenna (as unlike e.g. USB connectors, they have no through-hole element to anchor them solidly to the board). Seeed have a section on installing and removing such antennas [here](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/#installation-of-antenna) - they make it look easy, but that hasn't been my experience.

### Power

A significant downside to the Xiao boards is that if you intend to power them via the 5V pin then you need to wire in a diode between your 5V pin and this source (as described [here](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/#power-pins).

The Adafruit board has a similar issue but in this case, you can provide power via the battery pins on the back of the board (as described [here](https://learn.adafruit.com/adafruit-qt-py-esp32-c3-wifi-dev-board?view=all#power-3112671)) which do have the relevant diode protection.

I'm not sure why the battery pads on the Adafruit board have the diode and those on the Xiao boards do not (TODO: double check this). I _suspect_ that the downside of the diode on the Adafruit board is that a rechargeable lithium battery connected to these pins cannot be recharged via the board's USB port (no mention is made of charging in the Adafruit documentation), i.e. you'd have to disconnect the battery to recharge it with a separated device whereas you clearly can recharge such a battery via the the Xiao board's USB port (as described [here](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/#battery-usage).

A simple alternative that doesn't require worrying about diodes is to power the board via a simple 2-pin power-to-USB adapter.

TODO: include picture of board powered in this way.

TODO: confirm if the Waveshare, WeAct and Sparkfun boards have pins with the relevant diode:

* [Waveshare schematic](https://files.waveshare.com/wiki/ESP32-C3-Zero/ESP32-C3-Zero-Sch.pdf).
* [Sparkfun schematic](docs/sparkfun-dev-esp32-c3-mini-schematic.pdf) (produced with the [Altium viewer](https://www.altium.com/viewer/) from [`SparkFun_Pro_Micro.sch`](https://github.com/sparkfun/SparkFun_Pro_Micro-ESP32C3/blob/main/Hardware/SparkFun_Dev_ESP32_C3_MINI.sch)).
* [WeAct schematic](https://github.com/WeActStudio/WeActStudio.ESP32C3CoreBoard/blob/master/Hardware/WeAct-ESP32C3CoreBoard_V10_SchDoc.pdf).

TODO: I suspect it's simpler just to use USB power for every board rather than worrying about diode or no-diode.

Alternatives
------------

TODO:

* WeAct boards
* 433 boards
* Kickstarter board
* Telemetry radios.

---

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

Note: there's another package on PyPi called [`mpremote2`](https://pypi.org/project/mpremote2/) but it's not mentioned in the MicroPython docs, I can't find any reference to it in the MicroPython repository, and it's not released by the same maintainers as those listed for [`mpremote`](https://pypi.org/project/mpremote/).

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

If a program is running, and you connect to the REPL, you'll have to press `ctrl-C` to stop the program and get to the REPL prompt.

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

Instead of using shortcuts, I just used shell variables like so and associated a more obvious name with the two boards I had connected (a classic ESP32 board and a C3 board):

```
(env) $ classic='connect port:/dev/ch340-usb-serial'
(env) $ c3='connect /dev/esp-usb-serial'
```

Then I created [`dev/led_and_button.py`](dev/led_and_button.py) and could copy it to the appropriate board, reset the board and connect to its REPL all in one go like so for the C3 board:

```
(env) $ mpremote $c3 cp led_and_button.py :main.py + reset + repl
```

If you look at [`led_and_button.py`](dev/led_and_button.py), you'll see `BUTTON_PIN = 9` - the `BOOT` button on the board is connected to pin 9 and once the board has started, the `BOOT` button can be used as a normal button (it only does something special if held down while the board is starting up).

So, if `led_and_button.py` is running, and you're connected to the board, it'll print out the current value (1 or 0) of the `BOOT` button each time you press or release it.

Client and server
-----------------

Server:

```
$ classic='connect port:/dev/ch340-usb-serial'
$ mpremote $classic cp server.py :main.py + reset + repl
```

Client:

```
$ c3='connect /dev/esp-usb-serial'
$ mpremote $c3 cp client.py :main.py + reset + repl
```

SSID and passphrase
-------------------

Using just the 26 letters and the 10 digits, you can create base 36 values.

You need a 25 digit base 36 value to encode a UUID.

Generate ten of these with [random.org](https://www.random.org/strings/?num=10&len=25&digits=on&loweralpha=on&unique=on&format=html&rnd=new) and choose any two, one as the SSID and one as the passphrase, and update the `SSID` and `PASSPHRASE` values in both [`server.py`](server.py) and [`client.py`](client.py).

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

At the moment I'm unconvinced there's anything to be gained using the `select.poll` vs just a hard loop of non-blocking reads.

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

Development
-----------

I asked two questions about using UART0, i.e. the UART that runs over the board's USB port. The replies to both weren't particularly useful (I don't think I was well understood on either) but they worked well for [rubberducking](https://en.wikipedia.org/wiki/Rubber_duck_debugging).

I asked the first question [here](https://github.com/orgs/micropython/discussions/13696) on the in the ESP32 section of the MicroPython discussion forums. At this point I didn't yet understand that while one could create a `machine.UART` instance for UART0, it wasn't actually useful for anything beyond reconfiguring _some_ of the attributes associated with `sys.stdin` and `sys.stdout` and was not directly useful itself (e.g. one cannot call `read` or `write` on it).

My second question is [here](https://github.com/micropython/micropython/issues/6862#issuecomment-1958038625), I added it as a comment on the existing issue [_ESP32 UART 0 changing the baudrate #6862_](https://github.com/micropython/micropython/issues/6862). My [second comment](https://github.com/micropython/micropython/issues/6862#issuecomment-1959075926) there, summarizes my current understanding of things.

Once one understands that one can change the UART0 baud rate through the `machine.UART` constructor or its `init` method but that one then has to work with `sys.stdin` and `sys.stdout` (and that non-blocking reading seems not be currently supported), then the only important thing to be aware of is that the following error is harmless:

```
E (3769) uart: uart_wait_tx_done(1115): uart driver error
```

Each time, I tried to alter the baud rate, MicroPython output this error. I thought this meant things hadn't worked, but actually it appears to be harmless and is output whenever you change some attribute or other of UART0.

### Development scripts

I developed a number of small scripts/programs that are included in this repo.

As I often work with multiple boards, I generally create shell variables to let me easily distinguish between them when using `mpremote`, like so:

```
$ client='connect /dev/ttyACM0'
$ server='connect /dev/ttyACM1'
$ mpremote $server cp server.py :main.py + reset
$ mpremote $client cp client.py :main.py + reset
```

So, below wherever you see `$esp32c3` take it as having been set up to expand to `connect /dev/ttyACM0` (or whatever port the board is connected to).

#### LED and button

The [`dev/led_and_button.py`](dev/led_and_button.py) script demos using the board's LED and BOOT button. This is useful if you need some simple input and output. The pin values in the script work on both my WeAct C3 board and my no-name Super Mini C3 board.

```
$ mpremote $esp32c3 cp led_and_button.py :main.py + reset + repl
```

The LED will blink on and off and if you press the BOOT button, you'll see 1 or 0 being output.

The [`dev/led_interrupt.py`](dev/led_interrupt.py) script demos using a timer to blink the LED while the MCU is doing something else:

```
$ mpremote $esp32c3 cp led_interrupt.py :main.py + reset
```

The LED blinks even while the device is sleeping.

### Serial tester

[`dev/serial-tester.py`](dev/serial-tester.py) is a program that's meant to be run on your laptop and desktop, and it used in combination with all the following scripts to test serial port through put.

It requires two arguments:

* `--port`, e.g. `--port /dev/ttyACM0`
* `--baud-rate`, e.g. `--baud-rate 115200`

It then writes out blocks of bytes with a particular structure (with a timestamp and a CRC) and expects to receive similar blocks back. At intervals, it then out it then outputs statistics about throughput and errors. If the connected hardware isn't doing its job or is overwhelmed and generates invalid blocks then this program will spam your terminal with `?` characters and `Desynced` warnings or just sit there dumbly if it gets no input at all.

The logic is slightly more complicated than you might expect as it paces itself in writing to the given port rather than just writing as fast as it can. This is because the underlying system buffers are surprisingly large so, one can essentially write at huge speeds for short bursts before being blocked for long periods as the underlying bytes are written out (for reasons that aren't clear to me, you can write a lot of data and are then blocked for a long period as if the underlying buffer has to completely clear before you can write again, I would have expected that one could fill the buffer initially and then wait much shorter periods as small blocks of the underlying buffer become free that one can then write to).

The start-stop nature of letting the system block you as you hit buffer limits results in program that's in a continuous cycle of freezing and recovering. So, instead the program calculates the maximum rate it can transmit as given the current baud rate and paces itself accordingly.

TODO: include photo of two CP2102N serial-to-USB converters connected to each other and plugging into a USB hub. Then explain that one can run two instances of `serial-tester.py`, one talking to each converter and demonstrate the simplest case of just pumping serial data between two USB ports on your desktop/laptop.

### UART1 scripts

| C3 and USB-to-serial converter                       | Close-up                                                               |
|------------------------------------------------------|------------------------------------------------------------------------|
| ![uart1-to-converter](images/uart1-to-converter.jpg) | ![uart1-to-converter-close-up](images/uart1-to-converter-close-up.jpg) |

Note: in the pictures just the RX and TX pins are connected. Normally, you'd also connect the ground pins but here everything is already has a common ground so this isn't necessary.

These scripts are very simple and just read data from UART1 and echo it back, with UART1 is set up to use pins 20 and 21.

Somewhat confusingly, these are the pins labelled RX0 and TX0 on my WeAct C3 board - confusing because unlike a classic ESP32 where these are just the same pins as the ones that are wired through to the board's serial-to-USB converter chip, i.e. UART0, these pins do not correspond to UART0 so, I think, '0' shouldn't be included in labelling these pins.

These scripts, like the others below, bundle the main logic into an apparently pointless `run()` function - this is because of the difference in handling of global variables and variables with global scope (see notes on MicroPython specific speed optimizations above). Be careful to also use `micropython.const` with any values that aren't just used in one-off setup tasks, e.g. if you declare a global variable `BUFFER_SIZE` and then use it in one of the tight loops of these programs.

The [`dev/uart1_demo.py`](dev/uart1_demo.py) is the simplest, just copy it to a ESP32 C3 board that's connected to a USB-to-serial converter as shown above:

```
$ mpremote $esp32c3 cp uart1_demo.py :main.py + reset + repl
```

This and the other UART1 script are nice because you can leave `mpremote` running in `repl` mode and watch for any errors there.

With the board plugged into one USB port (and e.g. appearing as port `/dev/ttyACM0`) and the serial-to-USB converter plugged into another (and e.g. appearing as port `/dev/ttyACM1`), run the `serial-tester.py` program against the port correspond to the serial-to-USB converter with e.g. `--port /dev/ACM1 --baud-rate 1843200` where the specified baud rate matches that seen at the top of `uart1_demo.py`:

```
BAUD_RATE = 1843200
```

If all goes well, the `serial-tester.py` program should, after several seconds, output something like this:

```
.........
Effective speed: 1,779,852 bps
Blocks received: 13906
Latencies: min=1 ms, median=2 ms, max=4 ms
Bad CRCs: 0
Desynced: 0
Discarded: 0
```

You can try adjusting the `BAUD_RATE` value in the script (to the various common baud rates, i.e. 9600, 19200, 38400, 57600, 112500, 230400, 460800, 921600 and 1843200) and remembering to also update the `--baud-rate` argument passed to `serial-tester.py`.

I found the hardware UART connected like this to a serial-to-UART converter had no problem reaching the maximum speed supported by my converter, i.e. 1843200.

The other UART1 script is [`dev/uart1_demo_poller.py`](dev/uart1_demo_poller.py) is just the same script but rewritten to use [`Poll.ipoll`](https://docs.micropython.org/en/latest/library/select.html#select.poll.ipoll).

### UART0 scripts

This setup is simpler and just involves the board on its own without a serial-to-USB converter:

![c3](images/c3.jpg)

Working with UART1 worked exactly as expected. Working with UART0 proved to be more involved. It's the UART used for communication via the board's USB port and is used by the MicroPython REPL. While you can create a `machine.UART` instance corresponding to UART0, you have to work with it (as noted above) via `sys.stdin` and `sys.stdout`.

The fact that the original ESP32 didn't come with built-in USB support means that with classic USB boards performance depends on whatever serial-to-USB chip the board manufacturer chose to use on their board. The S and C series chips come with built-in USB support.

Compared to UART1, I got very poor through-put with UART0 - with my classic ESP32 board maxing out at around 115200 baud and my ESP32 C3 boards maxed out at around 230400 baud. The reasons the C3 boards maxed out at such low speeds is, I believe, to the lack of non-blocking support for `sys.stdin` that force you to use `Poll` and a byte-at-a-time reading in order to get non-blocking like behavior. _I think_ working a byte-at-a-time rather than being able to read as many bytes as are currently available into a buffer in one operation (as one can with UART1) is what results in the far lower maximum through puts.

Using UART0 and disabling ctrl-C (as one has to if one wants to send binary data as pressing ctrl-C is just the same as sending the byte 0x03) makes working with these scripts much more of a nuisance than working with UART1. You essentially disable your ability to return to the REPL and upload further scripts.

So, I often included something like the following at the top of these scripts:

```
# Give myself a chance to bail and upload a new program.
print('Press ctrl-C now to exit')
time.sleep(3)
print("Taking control of the USB UART")
time.sleep_ms(200)
```

I.e. these lines give me 3 seconds to press ctrl-C and retake control of the board before the program runs on to take the USB port for itself (or at least the virtual serial port aspect of things). So, I'd hit the board's RESET button and quickly do:

```
$ mpremote $esp32c3 repl
```

And press ctrl-C and so then be able to upload my next script. But if you do this, remember to only start `serial-tester.py` once the 3 seconds are up.

The first script is the simplest, it wraps the unusual behavior of UART0 up into the class `UsbUart0` (found in [`dev/usb_uart0.py`](dev/usb_uart0.py)) and then demos it with [`dev/usb_uart0_class_demo.py`](dev/usb_uart0_class_demo.py):

```
$ mpremote $esp32c3 cp usb_uart0.py : + cp usb_uart0_class_demo.py :main.py + reset
```

As before the script contains a `BAUD_RATE` value. This time there's no serial-to-USB converter involved - you just run the `serial-tester.py` program against the port corresponding to the board.

If you get into a state where you can't interact with the board with `mpremote` the only solution is to erase the chip and reflash MicroPython - erasing the chip first is important as otherwise the script that's taking control of UART0 will survive the reflashing process and start running again immediately. So, for a C3 board, this would involve:

```
$ port=/dev/ttyACM0
$ esptool.py --chip esp32c3 --port $port erase_flash
$ esptool.py --chip esp32c3 --port $port --baud 460800 write_flash -z 0x0 ESP32_GENERIC_C3-20240105-v1.22.1.bin
```

In the end, I decided the `UsbUart0` class didn't buy much and switched to doing everything in the single script [`dev/usb_uart0_demo.py`](dev/usb_uart0_demo.py) which can be used in the same way as the previous scripts:

```
$ mpremote $esp32c3 cp usb_uart0.py : + cp usb_uart0_demo.py :main.py + reset
```

And run `serial-tester.py` with its baud rate matching the `BAUD_RATE` in the `usb_uart0_demo.py`.

This script is a little fancier in that it wraps the main loop in a `try`, if an exception occurs it store it in a variable named `failure` and restores the normal UART0 baud rate and ctrl-C behavior so that you can connect to the REPL and e.g. do `print(failure)`.

In practice, I never hit any exceptions with this code.

The final script, in this section, is [`dev/usb_uart0_demo_buffered.py`](dev/usb_uart0_demo_buffered.py), where I experimented with caching object references (see optimization notes elsewhere in this document) and buffering the read bytes so that more than one could be written out per `write` call. These changes did **not** improve performance.
