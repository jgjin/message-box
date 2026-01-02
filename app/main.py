import time
import network
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import Pin, SPI, PWM
import config
import secrets
import urequests
import esp


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


bgcolor = color565(0, 0, 255)


def main():
    if setup_wifi() == False:
        return

    current_message = None
    i = 0

    lower_flag()
    time.sleep(1)

    while True:
        new_message = None
        try:
            new_message = urequests.get(config.SERVER_URL).content.decode("utf-8")
        except:
            pass

        if new_message != current_message:
            raise_flag()
            current_message = new_message
            display.clear(bgcolor)
            if current_message == None:
                display.draw_text8x8(
                    0,
                    0,
                    "<UNKNOWN>",
                    color565(255, 255, 255),
                    background=color565(255, 0, 0),
                )
            else:
                if len(current_message) > 0:
                    display.draw_text8x8(
                        10,
                        10,
                        current_message,
                        color565(255, 255, 255),
                        background=bgcolor,
                    )


        t = touch.raw_touch()
        print(t)
        if t != None:
            lower_flag()
            display.draw_text8x8(
                10, 30, "Touched: yes", color565(255, 255, 255), background=bgcolor
            )
        else:
            display.draw_text8x8(
                10, 30, "Touched: no ", color565(255, 255, 255), background=bgcolor
            )

        time.sleep(0.5)


main()
