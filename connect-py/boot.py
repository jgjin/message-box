import network
import time

import secrets

def connect_wifi(
    ssid: str,
    password: str,
    timeout_seconds: int = 30,
):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print("Connecting to Wi-Fi...")
    wlan.connect(ssid, password)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout_seconds:
            print("Wi-Fi connection failed!")
            return
        time.sleep(0.5)

    print("Wi-Fi connected, IP:", wlan.ifconfig()[0])

connect_wifi(secrets.SSID, secrets.PASSWORD, timeout_seconds=6)
