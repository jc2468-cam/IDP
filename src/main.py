from config import *

from interface.interface import *
from interface.base_output import *
from calibrations import *
from interface.linefollowing import LineSensor
# from interface.shortestpath import *

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



turns = [1, 1, 1, 0, 1] * 3
path = [("t", 1), ("t", 0), ("t", -1), ("t", -1), ("t", 1), ("t", 1)]
pos = 0

dt = 0.2
v_f = 0.8
tank = TrackedTank.default(AXLE_LENGTH, 6.5)

MODE = 1
if MODE == 0:
    line_sensors = LineSensor(tank, 9, 10, 11, 12)
    line_sensors.line_follow(v_f, dt)
    line_sensors.find_path(4, 62)

    """def next_junction(t):
        print("hello")
        global enabled
        global line_sensors, pos, turns
        
        def reactivate(t):
            global enabled, line_sensors
            enabled = True
            line_sensors.bending = False

            line_sensors.line_follow(v_f, dt)
        
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
elif MODE == 1:
    sensor1 = DigitalInput(9)
    sensor2 = DigitalInput(10)
    sensor3 = DigitalInput(11)
    sensor4 = DigitalInput(12)
    while True:
        while sensor1.value() == 0 and sensor4.value() == 0:
            v_r = 0.017 * (sensor2.value() - sensor3.value())
            if OUTPUT_MODE == 1 or OUTPUT_MODE == 2:
                print("pos:", tank.tick(dt))
            tank.drive(v_f, v_r)
            sleep(dt)
        print("pos:", tank.tick(dt))
        command = path[pos][0]
        value = path[pos][1]
        print("Junction Detected", command, value)
        if command == "t":
            sleep(0.3)
            print("pos:", tank.tick(0.3))
            if value != 0:
                tank.spin(value * 0.75)
                print("Spinning")
                sleep(0.95)
                print("pos:", tank.tick(0.95))
        elif command == "r":
            tank.drive(-v_f)
            sleep(1.25)
            print("pos:", tank.tick(1.25))
            tank.spin(1)
            sleep(1.5)
            print("pos:", tank.tick(1.5))
            tank.stop()
        sleep(2)
        pos += 1
        if pos == len(path):
            tank.stop()
            break
    while True:
        pass
elif MODE == 2:
    tank.drive(0.6, -0.02)
    for _ in range(50):
        print("pos:", tank.tick(dt))
        sleep(dt)
