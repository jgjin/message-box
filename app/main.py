import time
import network
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import Pin, SPI, PWM
import config
import secrets


def log_debug(s):
    print("DEBUG:", time.time(), s)


def log_error(s):
    print("ERROR:", time.time(), s)


display_spi = SPI(
    1, baudrate=40000000, sck=Pin(config.GPIO_SCK), mosi=Pin(config.GPIO_MOSI)
)
display = Display(
    display_spi,
    dc=Pin(config.GPIO_DC),
    cs=Pin(config.GPIO_CS),
    rst=Pin(config.GPIO_RST),
)

servo_pwm = PWM(Pin(config.GPIO_SERVO), freq=50)

touch_spi = SPI(2, baudrate=5_000_000, sck=Pin(4), mosi=Pin(5), miso=Pin(6))
touch = Touch(spi=touch_spi, cs=Pin(7), int_pin=Pin(8))


def setup_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    log_debug("Connecting to Wi-Fi")
    wlan.connect(secrets.SSID, secrets.PASSWORD)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > config.WIFI_CONNECT_TIMEOUT:
            # FIXME: display this on the screen
            log_error("WiFi connection failed")
            log_error("Reset the machine to try connecting again")
            return False
        time.sleep(0.5)

    log_debug("WiFi connected with IP: " + wlan.ifconfig()[0])
    return True


def lower_flag():
    servo_pwm.duty(26)


def raise_flag():
    servo_pwm.duty(77)


lower_flag()
flag_rasied = False


def main():
    if setup_wifi() == False:
        return

    current_message = ""
    i = 0
    while True:
        print(i)
        display.clear(color565(255, 255, i))
        display.draw_text8x8(0, 0, "Hello", color565(255,255,255))
        i = (i + 1) % 256
        time.sleep(0.125)
        print(touch.get_touch())
        if i % 16 == 0:
            if lowered:
                lowered = not lowered
                raise_flag()
            else:
                lowered = not lowered
                lower_flag()


main()
