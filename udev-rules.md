ESP32-C3 Core
-------------

`/var/log/syslog` output on initially connecting an ESP32-C3 Core:

```
kernel: [  548.742226] usb 1-7.4: new full-speed USB device number 7 using xhci_hcd
kernel: [  548.844473] usb 1-7.4: New USB device found, idVendor=303a, idProduct=1001, bcdDevice= 1.01
kernel: [  548.844486] usb 1-7.4: New USB device strings: Mfr=1, Product=2, SerialNumber=3
kernel: [  548.844491] usb 1-7.4: Product: USB JTAG/serial debug unit
kernel: [  548.844496] usb 1-7.4: Manufacturer: Espressif
kernel: [  548.844499] usb 1-7.4: SerialNumber: 60:55:F9:AF:94:88
mtp-probe: checking bus 1, device 7: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.4"
mtp-probe: bus: 1, device: 7 was not an MTP device
kernel: [  548.900678] cdc_acm 1-7.4:1.0: ttyACM0: USB ACM device
kernel: [  548.900725] usbcore: registered new interface driver cdc_acm
kernel: [  548.900726] cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
mtp-probe: checking bus 1, device 7: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.4"
```

Rule to add to `/etc/udev/rules.d/50-serial-ports.rules`:

```
# ESP32-C3 Core
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", \
    SYMLINK+="esp-usb-serial", MODE="0666"

ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", ENV{MTP_NO_PROBE}="1"
```

### Multiple devices

If you change the `SYMLINK` rule to:

```
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", \
    SYMLINK+="esp-usb-serial esp-usb-serial%n", MODE="0666"
                             ^^^^^^^^^^^^^^^^
```

Then, if multiple devices are connected, each one gets a unique name with a number at the end, e.g. `esp-usb-serial0`, and the last one connected gets the name `esp-usb-serial` (taking it from any previous device with the same `ATTRS`).


ESP32 Core
----------

`/var/log/syslog` output on initially connecting an ESP32 Core:

```
kernel: [ 1029.249903] usb 1-7.1: new full-speed USB device number 8 using xhci_hcd
kernel: [ 1029.351792] usb 1-7.1: New USB device found, idVendor=1a86, idProduct=7522, bcdDevice= 2.64
kernel: [ 1029.351805] usb 1-7.1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
kernel: [ 1029.351810] usb 1-7.1: Product: USB Serial
mtp-probe: checking bus 1, device 8: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.1"
mtp-probe: bus: 1, device: 8 was not an MTP device
kernel: [ 1029.386273] usbcore: registered new interface driver usbserial_generic
kernel: [ 1029.386283] usbserial: USB Serial support registered for generic
kernel: [ 1029.387521] usbcore: registered new interface driver ch341
kernel: [ 1029.387530] usbserial: USB Serial support registered for ch341-uart
kernel: [ 1029.387549] ch341 1-7.1:1.0: ch341-uart converter detected
kernel: [ 1029.388142] usb 1-7.1: ch341-uart converter now attached to ttyUSB0
mtp-probe: checking bus 1, device 8: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.1"
mtp-probe: bus: 1, device: 8 was not an MTP device
snapd[1014]: hotplug.go:200: hotplug device add event ignored, enable experimental.hotplug
ModemManager[1066]: <info>  [base-manager] couldn't check support for device '/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.1': not supported by any plugin
```

Rule to add to `/etc/udev/rules.d/50-serial-ports.rules`:

```
# ESP32 Core
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7522", \
    SYMLINK+="ch340-usb-serial", MODE="0666"

ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7522", ENV{MTP_NO_PROBE}="1"
ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7522", ENV{ID_MM_DEVICE_IGNORE}="1"
```

WCH CH343P UART to serial
-------------------------

`/var/log/syslog` output:

```
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.402439] usb 1-7.1: new full-speed USB device number 7 using xhci_hcd
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.504798] usb 1-7.1: New USB device found, idVendor=1a86, idProduct=55d3, bcdDevice= 4.45
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.504812] usb 1-7.1: New USB device strings: Mfr=0, Product=2, SerialNumber=3
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.504817] usb 1-7.1: Product: USB Single Serial
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.504820] usb 1-7.1: SerialNumber: 5735013554
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx mtp-probe: checking bus 1, device 7: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.1"
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx mtp-probe: bus: 1, device: 7 was not an MTP device
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.557155] cdc_acm 1-7.1:1.0: ttyACM0: USB ACM device
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.557221] usbcore: registered new interface driver cdc_acm
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx kernel: [11758.557226] cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx mtp-probe: checking bus 1, device 7: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.1"
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx mtp-probe: bus: 1, device: 7 was not an MTP device
May  9 15:22:03 joebloggs-OMEN-25L-Desktop-GT12-0xxx snapd[955]: hotplug.go:200: hotplug device add event ignored, enable experimental.hotplug
May  9 15:22:06 joebloggs-OMEN-25L-Desktop-GT12-0xxx ModemManager[1001]: <info>  [base-manager] couldn't check support for device '/sys/devices/pci0000:00/0000:00:14.0/usb1/1-7/1-7.1': not supported by any plugin
```

Rule to add to `/etc/udev/rules.d/50-serial-ports.rules`:

```
# WCH CH343P
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d3", \
    SYMLINK+="ch343p-usb-serial", MODE="0660", TAG+="uaccess"

ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d3", ENV{MTP_NO_PROBE}="1"
ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d3", ENV{ID_MM_DEVICE_IGNORE}="1"
```

**Notice** the use of `0660`, rather than `0666`, for `MODE` - this makes it read/write only to the ower - `root` - and the group - `dialout`, but then the `TAG+="uaccess"` magic also makes it accessible to the loggen-in user.

You can check this out like so:

```
$ ls -l /dev/ch343p-usb-serial
lrwxrwxrwx 1 root root 7 May  9 15:38 /dev/ch343p-usb-serial -> ttyACM0
$ ls -l /dev/ttyACM0
crw-rw----+ 1 root dialout 166, 0 May  9 15:38 /dev/ttyACM0
$ getfacl /dev/ttyACM0
getfacl: Removing leading '/' from absolute path names
# file: dev/ttyACM0
# owner: root
# group: dialout
user::rw-
user:joebloggs:rw-
group::rw-
mask::rw-
other::---
```

The `+` shown for `/dev/ttyACM0` means there's additional ACL information associated with file and `getfacl` then shows that, among other things, these mean that the logged in user - `joebloggs` - can read and write the file.

This is the modern way to do things and comes from the Arch Linux wiki section on ["allowing regular users to use devices"](https://wiki.archlinux.org/title/udev#Allowing_regular_users_to_use_devices).
