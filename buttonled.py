# buttonled.py

from machine import Pin, PWM
from random import randint
import uasyncio

# Define PWM pins globally
pins = [1, 2, 4]
freq_num = 10000
pwm0 = PWM(Pin(pins[0]))
pwm1 = PWM(Pin(pins[1]))
pwm2 = PWM(Pin(pins[2]))
pwm0.freq(freq_num)
pwm1.freq(freq_num)
pwm2.freq(freq_num)

def setColor(r, g, b):
    global pwm0, pwm1, pwm2
    pwm0.duty_u16(65535 - r)
    pwm1.duty_u16(65535 - g)
    pwm2.duty_u16(65535 - b)

async def run_led():
    try:
        while True:
            red = randint(0, 65535)
            green = randint(0, 65535)
            blue = randint(0, 65535)
            setColor(red, blue, green)
            await uasyncio.sleep_ms(200)
    except KeyboardInterrupt:
        pwm0.deinit()
        pwm1.deinit()
        pwm2.deinit()
