import time
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import Pin, SPI, PWM
import config

display_spi = SPI(1, baudrate=40000000, sck=Pin(config.GPIO_SCK), mosi=Pin(config.GPIO_MOSI))
display = Display(display_spi, dc=Pin(config.GPIO_DC), cs=Pin(config.GPIO_CS), rst=Pin(config.GPIO_RST))

servo_pwm = PWM(Pin(config.GPIO_SERVO), freq=50)


def handle_touch(x, y):
    print("Touched at ", x, y)


touch_spi = SPI(2, baudrate=5_000_000, sck=Pin(4), mosi=Pin(5), miso=Pin(6))
touch = Touch(spi=touch_spi, cs=Pin(7), int_pin=Pin(8)) # , int_hander=handle_touch)


def lower_flag():
    servo_pwm.duty(26)


def raise_flag():
    servo_pwm.duty(77)


def bad():
    i = 0
    lowered = False
    while True:
        print(i)
        i = (i + 1) % 256
        display.clear(color565(0, 0, i))
        time.sleep(0.125)
        print(touch.get_touch())
        if i % 16 == 0:
            if lowered:
                lowered = not lowered
                raise_flag()
            else:
                lowered = not lowered
                lower_flag()


def main():
    while True:
        raise_flag()
        time.sleep(2)
        lower_flag()
        time.sleep(2)


bad()
