import network
import time

# My ESP32 takes less than 2 seconds to join, so 8s is a long timeout.
_CONNECT_TIMEOUT = 8000
_RETRY_INTERVAL = 5


def create_ap(ssid, passphrase):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # Note: the classic ESP32 does not support AUTH_WPA3_PSK.
    ap.config(ssid=ssid, key=passphrase, security=network.AUTH_WPA2_PSK)
    ap_address = ap.ifconfig()[0]
    print(f"started access point with SSID {ssid} and address {ap_address}")


def connect_to_ap(ssid, passphrase):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    def is_connected():
        start = time.ticks_ms()
        while True:
            if sta.isconnected():
                return True
            diff = time.ticks_diff(time.ticks_ms(), start)
            if diff > _CONNECT_TIMEOUT:
                sta.disconnect()
                return False

    while True:
        print(f"attempting to connect to SSID {ssid}")
        sta.connect(ssid, passphrase)
        if is_connected():
            address, _, gateway, *_ = sta.ifconfig()
            print(f"connected to access point {gateway} and was assigned address {address}")
            return address, gateway
        else:
            print(f"failed to connect - retrying in {_RETRY_INTERVAL} seconds")
            time.sleep(_RETRY_INTERVAL)
