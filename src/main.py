from interface import *
from calibrations import *
from col_sense import *
from utime import sleep, ticks_ms

from machine import Pin, PWM, Timer, I2C


#i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
#print(i2c_bus.scan())
#tcs = TCS34725(i2c_bus)

#print('raw: {}'.format(tcs.read('raw')))

#print('rgb: {}'.format(tcs.read('rgb')))

tank = TrackedTank.default(10.0, 6.5)

tank.drive(0.5)

dt = 0.1
while True:
    sleep(dt)
    print("pos:", tank.tick(dt))

