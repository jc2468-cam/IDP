from config import *

from interface.interface import *
from interface.base_output import *
from calibrations import *
from interface.linefollowing import LineSensor

from utime import sleep, ticks_ms
from machine import Pin, PWM, Timer, I2C

if AWAIT_LINK:
    while input().strip() != "Control::start":
        pass
    param_command = input().strip()
    if param_command == "Control::fetch_params":
        print(f"Control::return_params({WHEEL_DIAM}, {MOTOR_CAL_M}, {MOTOR_CAL_C}, {MOTOR_CAL_T})")
    else:
        print("Got param command", param_command)

#i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
#print(i2c_bus.scan())
#tcs = TCS34725(i2c_bus)

#print('raw: {}'.format(tcs.read('raw')))

#print('rgb: {}'.format(tcs.read('rgb')))

# dt = 0.3
# tank = TrackedTank.default(AXLE_LENGTH, 6.5)
# line_sensors = LineSensor(tank, 9, 10, 11, 12)
# line_sensors.line_follow(0.45, dt)

m0 = Motor(0)
m0.run(-1)

s1 = Servo(0)
for _ in range(3):
    s1.set_position(0.7)
    sleep(3)
    s1.set_position(0.0)
    sleep(3)
m0.off()

# tank.drive(0.7)
# for _ in range(20):
#     sleep(dt)
#     print("pos:", tank.tick(dt))
# tank.drive(0.7, 0.02, 0.0)
# for _ in range(20):
#     sleep(dt)
#     print("pos:", tank.tick(dt))
# tank.drive(0.7)
# for _ in range(20):
#     sleep(dt)
#     print("pos:", tank.tick(dt))
# tank.stop()
