from config import *

from interface.interface import *
from interface.base_output import *
from calibrations import *
from interface.linefollowing import LineSensor

from utime import sleep, ticks_ms
from machine import Pin, PWM, Timer, I2C


if AWAIT_LINK:
    print("AWAITING LINK")
    while input().strip() != "Control::start":
        pass
    param_command = input().strip()
    if param_command == "Control::fetch_params":
        print(f"Control::return_params({WHEEL_DIAM}, {MOTOR_CAL_M}, {MOTOR_CAL_C}, {MOTOR_CAL_T})")
    else:
        print("Got param command", param_command)

if INPUT_MODE == 1 or INPUT_MODE == 2:
    start_input_sim_monitor()

#i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
#print(i2c_bus.scan())
#tcs = TCS34725(i2c_bus)

#print('raw: {}'.format(tcs.read('raw')))

#print('rgb: {}'.format(tcs.read('rgb')))

dt = 0.1
tank = TrackedTank.default(AXLE_LENGTH, 6.5)
line_sensors = LineSensor(tank, 9, 10, 11, 12)
line_sensors.line_follow(0.45, dt)

pos = 0
enabled = True

turns = [1, -1, 0, -1]

def next_junction():
    global enabled
    if enabled:
        enabled = False
        sleep(0.2)

        global linefollowing, pos, turns
        linefollowing.stop_following()

        linefollowing.tank.spin(turns[pos])
        pos += 1

        def reactivate(t):
            global enabled, linefollowing
            enabled = True

            linefollowing.line_follow(0.45, dt)

        timer = Timer()
        timer.init(mode=Timer.ONE_SHOT, period=3000, callback=reactivate)

line_sensors.sensor1.bind_interupt(next_junction, 1)
line_sensors.sensor4.bind_interupt(next_junction, 1)
