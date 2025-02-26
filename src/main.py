from interface import *
from calibrations import *
from col_sense import *
from utime import sleep, ticks_ms

from machine import Pin, PWM, Timer, I2C


motor = Motor(1)
led = Led(20)
led.blink_ticker(2.5)
#sensor = DigitalSensor(21)
sensor_pin = Pin(21, Pin.IN, Pin.PULL_DOWN)

motor_tacho(motor, sensor_pin, 100, 0.1, 0.3, 1.0)

i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
#print(i2c_bus.scan())
#tcs = TCS34725(i2c_bus)

#print('raw: {}'.format(tcs.read('raw')))

#print('rgb: {}'.format(tcs.read('rgb')))

while True:
    pass

