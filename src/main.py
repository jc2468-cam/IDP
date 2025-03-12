from config import *

from interface.interface import *
from interface.base_output import *
from calibrations import *
from interface.linefollowing import LineSensor
from interface.shortestpath import *

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

dt = 0.2
tank = TrackedTank.default(AXLE_LENGTH, 6.5)
line_sensors = LineSensor(tank, 9, 10, 11, 12)
line_sensors.line_follow(0.8, dt)
line_sensors.find_path(4, 62)

"""def next_junction(t):
    print("hello")
    global enabled
    global line_sensors, pos, turns
    
    def reactivate(t):
        global enabled, line_sensors
        enabled = True
        line_sensors.bending = False

        line_sensors.line_follow(0.8, dt)
    
    if enabled:
        enabled = False
        if turns[pos] != 0:
            line_sensors.bending = True
            #sleep(0.2)
            line_sensors.stop_follow()
            sleep(0.3)
            print("turning")
            line_sensors.tank.spin(turns[pos] * 0.75)
            timer = Timer()
            timer.init(mode=Timer.ONE_SHOT, period=950, callback=reactivate)
        else:
            print("skipping")
            sleep(0.2)
            enabled = True
        pos += 1"""

line_sensors.sensor1.bind_interupt(line_sensors.next_junction, 1)
line_sensors.sensor4.bind_interupt(line_sensors.next_junction, 1)
