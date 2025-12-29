import time
from ili9341 import Display, color565
from machine import Pin, SPI, PWM
import config

spi = SPI(1, baudrate=40000000, sck=Pin(config.SCK), mosi=Pin(config.MOSI))
display = Display(spi, dc=Pin(config.DC), cs=Pin(config.CS), rst=Pin(config.RST))

servo_pwm = PWM(Pin(config.SERVO), freq=50)


def lower_flag():
    servo_pwm.duty(26)
    # servo_pwm.duty_ns(500_000)


def raise_flag():
    servo_pwm.duty(77)
    # servo_pwm.duty_ns(1_500_000)


def bad():
    i = 0
    lowered = False
    while True:
        print(i)
        i = (i + 1) % 256
        display.clear(color565(0, 0, i))
        time.sleep(0.125)
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

main()
