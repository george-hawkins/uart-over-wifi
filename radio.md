There are no end of radio modules out there. Here, I only focus on those where the cost for a pair of communicating devices comes in at significantly less than the US$100 typical for a pair of classic Holybro [telemetry radios](https://holybro.com/collections/telemetry-radios/products/sik-telemetry-radio-v3).

Other criteria:

* Availability: for price, I've mainly gone with AliExpress stores but I only wanted modules available from multiple sources, not just AliExpress.
* Popularity: good open-source support for all modules covered and large community with plenty of YouTube videos and tutorials.

---

ESP32 S3/C3

Compare large(ish) Espressif S3 with Digikey antenna with Seeed Xiao C3 with Seeed antenna.

---

Waveshare RP240-Zero seems perfect dev board to go with modules with no builtin MCU: https://www.waveshare.com/wiki/RP2040-Zero / https://www.waveshare.com/rp2040-zero.htm?sku=20335

---

nRF with SMA connector and Pico
nRF with u.FL connector and Pico
[ Note existence of u.FL board without meandered antenna but no easy to solder pins ]

RF-Nano: https://www.aliexpress.com/item/1005005593408190.html have no FEM but according to https://www.youtube.com/watch?v=Ye1URyDRkiQ are good for 10m and others mention 20m to 30m.

Version with u.FL is useless (see notes elswhere already).

IMPORTANT: use AMS1117 even if you don't need the extra head-room _for the caps_:

* Video introducing small 3.3V adapter with caps: https://www.youtube.com/watch?v=Ye1URyDRkiQ from Anyone Can Build Robots!
* Video on wire-length and all the other things that can cause problems: https://www.youtube.com/watch?v=Z7_Cy66Vnrc from Electronoobs.

---

HC-12 - mention video about resolving range issue. Cf. range of Banggood and AliExpress modules.

The SX1280 is the 2.4GHz radio used in ELRS. It's 433 MHz abd 915 MHz siblings are the SX1278 and SX1276 respectively.

The SX1262 its newer improved sub-GHz radio (for details see Waveshare notes about it [here](https://www.waveshare.com/wiki/Core1262-868M)).

Paweł Spychalski uses the HC-12 as a telemetry radio:

* https://quadmeup.com/diy-wireless-telemetry-link-for-uav/
* https://quadmeup.com/hc-12-433mhz-rf-serial-module-range-test/

---

Waveshare: Pico plus SX1262 combo: https://www.waveshare.com/product/iot-communication/long-range-wireless/nb-iot-lora/rp2040-lora.htm?sku=26543

See also: https://www.waveshare.com/wiki/RP2040-LoRa

Note: it's not obvious initially but it does come with a whip antenna and USB daughter board.

---

Ai-Thinker: https://docs.ai-thinker.com/en/lora/man

RA-01 has pin for soldering on coil antenna
RA-02 has u.FL connector

On AliExpress (Simple Robot):

* All pins broken out: https://www.aliexpress.com/item/32824499318.html
* Only essential pins broken out: https://www.aliexpress.com/item/1005002808672088.html (see last variant).

Adafruit also carry this module and they have way more detail (e.g. about those essential/non-essential pins) and about RFM6x (FSK only) and RFM9x (FSX plus LoRa):

https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts

The bare modules (that Adafruit carry plus variants soldered to breakouts with level-shifters etc.) are available on AliExpress:

Shenzhen Duoweisi: https://www.aliexpress.com/item/1005006184943399.html

The modules above (from Simple Robot) are just more nicely packaged versions.

---

SX1262 plus ESP32-S3 plus screen combo - https://heltec.org/project/wifi-lora-32-v3/

Note: you can get it in a variant with a nice plastic shell.

AliExpress:

* https://www.aliexpress.com/item/1005005443005152.html
* https://www.aliexpress.com/item/1005004645530908.html (433MHz) / https://www.aliexpress.com/item/1005005574501142.html (915MHz)
* https://www.aliexpress.com/i/32882205132.html
* https://www.aliexpress.com/item/1005004971292330.html
* https://www.aliexpress.com/item/32886711232.html

Heltec also have modules for slightly less without screens, see:

* https://heltec.org/project/wireless-stick-lite-v2/
* https://www.aliexpress.com/item/1005004984658496.html

* https://ec-buying.aliexpress.com/store/1762106/pages/all-items.html?sortType=bestmatch_sort&SearchText=SX1262

---

ArduPilot have a long list of telemetry radio products and projects: <https://ardupilot.org/copter/docs/common-telemetry-landingpage.html>

There's also ELRS Airport: https://www.expresslrs.org/software/airport/ but my impression is that this videos reflects the common opinion of its current state: https://www.youtube.com/watch?v=f8jwl-f2RLA

But my impression is that the only serious open-source project is mLRS: https://github.com/olliw42/mLRS

It is targetted at long range but does support FSK and yet despite that, for reasons that aren't clear to me, lists relatively low maximum speeds: 56888/72888 bps up/down for 2.4 GHz and 25600/32800 bps up/down for 915/433 MHz.

The only ready-to-use modules seem to be: https://www.seeedstudio.com/LoRa-E5-mini-STM32WLE5JC-p-4869.html

At US$22 each, they're close to be excluded from my price criteria.

Huge support thread: https://www.rcgroups.com/forums/showthread.php?4037943
And Discord where OlliW is active: https://discord.gg/vwjzCD6ws5

---

Lillygo have:

* An older classic ESP32 plus SX1278/SX1276 plus screen: https://www.lilygo.cc/products/lora3
* A newer ESP32-S3 plus SX1262 plus screen: https://www.lilygo.cc/products/t3s3-v1-0 (for whatever reason it's also available in variants with the older radio modules and the 2,4GHz SX1280).

Note: Paxcounter / DisasterRadio are just examples that come pre-installed, it seems weird they make this a selectable option.

They're no cheaper on the Lillygo AliExpress store (and less choice):

* https://www.aliexpress.com/item/32872078587.html
* https://www.aliexpress.com/item/1005004627139838.html

---

Compare supposedly sleeved balun antennas from AliExpress with whips - I've only got sleeved baluns for 2.4GHz, i.e. just for use with ESP32.

---

2.4Ghz isn't a single frequency, it's a band.

If I power up my quad and talk to its 2.4GHz RX using my TX, my 2.4GHz home Wi-Fi network doesn't suddenly  go to hell.

If you feel having two different wireless technologies using the 2.4GHz band at the same time in close proximity must lead to disaster, then please test this in practice and provide data to back this up.

---

Breadboards and breadboard jumper wires don't well with RF.

It's not that you can't use them - there are no end of YouTube tutorials where everything is set up on a breadboard (e.g. [Arduino Wireless Communication – NRF24L01 Tutorial](https://www.youtube.com/watch?v=7rcVeFFHcFM) from How To Mechatronics) but you may experience hard to diagnose problems and an impact on range.

E.g. see issues discussed in Electronoobs's video linked above.

Hence perfboards from AliExpress. See videos on edge connectors here on Adafruit perfboard product page (they call them proto-boards): https://www.adafruit.com/product/4786

And see this Adafruit Learn project where they use a perfboard: https://learn.adafruit.com/step-switch-party/assemble-the-step-switch-party

See videos:

* How Do You? DIY: https://www.youtube.com/watch?v=l9Kbr8cPqOE

Find others and summarize key points, e.g. 1m 37s mark in How Do You? DIY video.

See May 7th videos: https://www.youtube.com/feed/history?query=perfboard

