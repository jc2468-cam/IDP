from config import *
from machine import I2C

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


tank = TrackedTank.default(AXLE_LENGTH, 6.5)
tank.stop()

actuator = Actuator(0)
servo = Servo(0)

#i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
# print(i2c_bus.scan())
#tcs = TCS34725(i2c_bus)

global MODE


def reverse_path(path):
    return [(a[0], -a[1]) for a in path[:-1:-1]]

def reverse_turns(path):
    started = False
    start_i, end_i = 0, 0
    for i in range(len(path)):
        if started:
            if path[i][0][0] != "t":
                end_i = i
        elif path[i][0][0] == "t":
            start_i = i
            started = True
    turns = [a[0] for a in path[start_i:end_i:-1]]
    extras = [a[1:] for a in path[start_i:end_i]]
    return path[:start_i] + [t + e for t, e in zip(turns, extras)] + path[end_i:]

test_location = 0

# start
front_house_start_path = [[("t", 0)], [("t", 1)], [("t", -1)], [("p", 0)]]

# [0] drop red, [1] drop blue
back_house_drop_path = [[[("t", -1)], [("t", -1)], [("t", -1)], [("t", 0)], [("t", 0)], [("t", 1)], [("d", 0)]], [[("t", -1)], [("t", -1)], [("t", 0)], [("d", 0)]]]
front_house_drop_path = [[[("t", -1)], [("t", 1)], [("d", 0)]], [[("t", 1)], [("t", 0)], [("t", -1)], [("d", 0)]]]
warehouse_drop_path = [[[("t", 1)], [("t", 0)], [("t", 1)], [("t", 0)], [("t", 0)], [("d", 0)]], [[("t", -1)], [("t", -1)], [("t", 0)], [("t", 0)], [("d", 0)]]]
factory_drop_path = [[[("t", -1)], [("t", -1)], [("t", 1)], [("t", 0)], [("d", 0)]], [[("t", -1)], [("t", 1)], [("t", 0)], [("t", -1)], [("t", 0)], [("d", 0)]]]
red_drop_blue_drop_path = [[("t", -1)], [("t", 0)], [("t", 0)], [("t", -1)], [("d", 0)]]
blue_drop_red_drop_path = [[("t", 1)], [("t", 0)], [("t", 0)], [("t", 1)], [("d", 0)]]

# return drop paths
red_drop_warehouse_path = reverse_path(warehouse_drop_path[0][:-1] + [[("p", 0)]])
red_drop_factory_path = reverse_path(factory_drop_path[0][:-1] + [[("p", 0)]])
red_drop_front_house_path = reverse_path(front_house_drop_path[0][:-1] + [[("p", 0)]])
red_drop_back_house_path = reverse_path(back_house_drop_path[0][:-1] + [[("p", 0)]])

blue_drop_warehouse_path = reverse_path(warehouse_drop_path[1][:-1] + [[("p", 0)]])
blue_drop_factory_path = reverse_path(factory_drop_path[1][:-1] + [[("p", 0)]])
blue_drop_front_house_path = reverse_path(front_house_drop_path[1][:-1] + [[("p", 0)]])
blue_drop_back_house_path = reverse_path(back_house_drop_path[1][:-1] + [[("p", 0)]])

# between
front_house_back_house_path = [[("t", -1)], [("t", -1)], [("t", -1)], [("t", 0)], [("t", 1), ("l", 0)], [("p", 0)]]
front_house_factory_path = [[("t", -1)], [("t", -1)], [("t", -1)], [("t", 1)], [("t", 1), ("l", 0)], [("p", 0)]]
front_house_warehouse_path = [[("t", -1)], [("t", -1)], [("t", 0)], [("t", -1)], [("t", 0)], [("t", -1), ("l", 0)], [("p", 0)]]

back_house_front_house_path = reverse_turns(front_house_back_house_path)
back_house_factory_path = [[("t", 1)], [("t", -1)], [("t", 1), ("l", 0)], [("p", 0)]]
back_house_warehouse_path = [[("t", 1)], [("t", -1)], [("t", 0)], [("t", -1)], [("t", -1), ("l", 0)], [("p", 0)]]

factory_front_house_path = reverse_turns(front_house_factory_path)
factory_back_house_path = reverse_turns(back_house_factory_path)
factory_warehouse_path = [[("t", 1)], [("t", -1)], [("t", -1), ("l", 0)], [("p", 0)]]

warehouse_front_house_path = reverse_turns(front_house_warehouse_path)
warehouse_back_house_path = reverse_turns(back_house_warehouse_path)
warehouse_factory_path = reverse_turns(factory_warehouse_path)

# position in path list
pos = 0
# position on board
location = "start"

dt = 0.07
v_f = 0.7
button = DigitalInput(8)
MODE = 3
line_sensors = LineSensor(tank, 9, 10, 11, 12, 1)
driving = False
range_sensor = I2C(1, scl=Pin(17), sda=Pin(16))

def begin(p=0):
    global MODE
    MODE = 1

#while MODE > 2:
    #button.bind_interupt(begin, 1)

if MODE == 0:
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
    print("driving mode 1")
    led = Led(1)
    sensor1 = DigitalInput(9)
    sensor2 = DigitalInput(10)
    sensor3 = DigitalInput(11)
    sensor4 = DigitalInput(12)
    led.on()
    # list of blocks on the rack
    # -1 for unknown, 0 for red, 1 for blue
    blocks = []
    active_block = 0
    servo_step = 2/3
    scheduled_extra = list()
    max_blocks = 2
    
    # weights matrix from floyds, needs updating
    weights = [[0, 284, 389, 52, 300, 0, 0], [304, 0, 179, 336, 188, 0, 0], [320, 179, 0, 347, 40, 0, 0], [52, 316, 357, 0, 332, 0, 0], [300, 168, 111, 332, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    test_path = ["front_house", "factory", "red_drop"]
    
    sleep(2)
    
    while True:
        if driving == False:
            pos = 0
            print("Getting path")
            if len(test_path) > 0:
                if test_location == 0:
                    next_location = "front_house"
                    path = front_house_start_path
                    test_location = 1
                else:
                    location = test_path[test_location - 1]
                    next_location = test_path[test_location]
                    test_location += 1
                if test_location == len(test_path):
                    tank.stop()
                print("Using test path")
                driving = True
            
            else:
                pos = 0

                if location == "start":
                    next_location = "front_house"
                    path = front_house_start_path

                if len(blocks) == max_blocks:
                    if 0 in blocks:
                        next_location = "red_drop"
                        if blocks[active_block] != 0:
                            counter = 0
                            for b in blocks:
                                if b != 0:
                                    counter += 1
                                else:
                                    break
                            servo.slow_set_position(0, servo_step * counter)
                    else:
                        next_location = "blue_drop"
                        
            if location == "warehouse":
                if next_location == "factory":
                    path = warehouse_factory_path
                if next_location == "front_house":
                    path = warehouse_front_house_path
                if next_location == "back_house":
                    path = warehouse_back_house_path
                if next_location == "red_drop":
                    path = warehouse_drop_path[0]
                if next_location == "blue_drop":
                    path = warehouse_drop_path[1]

            if location == "factory":
                if next_location == "warehouse":
                    path = factory_warehouse_path
                if next_location == "front_house":
                    path = factory_front_house_path
                if next_location == "back_house":
                    path = factory_back_house_path
                if next_location == "red_drop":
                    path = factory_drop_path[0]
                if next_location == "blue_drop":
                    path = factory_drop_path[1]

            if location == "front_house":
                if next_location == "warehouse":
                    path = front_house_warehouse_path
                if next_location == "factory":
                    path = front_house_factory_path
                if next_location == "back_house":
                    path = front_house_back_house_path
                if next_location == "red_drop":
                    path = front_house_drop_path[0]
                if next_location == "blue_drop":
                    path = front_house_drop_path[1]

            if location == "back_house":
                if next_location == "warehouse":
                    path = back_house_warehouse_path
                if next_location == "factory":
                    path = back_house_factory_path
                if next_location == "front_house":
                    path = back_house_factory_path
                if next_location == "red_drop":
                    path = back_house_drop_path[0]
                if next_location == "blue_drop":
                    path = back_house_drop_path[1]

            if location == "red_drop":
                if next_location == "warehouse":
                    path = red_drop_warehouse_path
                if next_location == "factory":
                    path = red_drop_factory_path
                if next_location == "front_house":
                    path = red_drop_front_house_path
                if next_location == "back_house":
                    path = red_drop_back_house_path
                if next_location == "blue_drop":
                    path = red_drop_blue_drop_path

            if location == "blue_drop":
                if next_location == "warehouse":
                    path = blue_drop_warehouse_path
                if next_location == "factory":
                    path = blue_drop_factory_path
                if next_location == "front_house":
                    path = blue_drop_factory_path
                if next_location == "back_house":
                    path = blue_drop_factory_path
                if next_location == "red_drop":
                    path = blue_drop_red_drop_path

                driving = True
                location = next_location

        if driving == True:
            while sensor1.value() == 0 and sensor4.value() == 0:
                v_r = -0.017 * (sensor2.value() - sensor3.value())
                if LOG_POSITION:
                    print("pos:", tank.tick(dt))
                tank.drive(v_f, v_r)
                sleep(dt)
            tank.log_sleep(dt)
            if pos == len(path):
                driving = False
            new_scheduled_extra = list()
            for instruction in path[pos] + scheduled_extra:
                command = instruction[0]
                value = instruction[1]
                print("Junction Detected", command, value)
                if command == "t":
                    sleep(0.2)
                    tank.log_tick(0.3)
                    if value > 0:
                        tank.spin(value * 0.9)
                        print("Spinning")
                        tank.log_sleep(0.6)
                    if value < 0:
                        tank.spin(value * 0.9)
                        print("Spinning")
                        tank.log_sleep(0.85)
                    else:
                        tank.log_sleep(0.3)
                    tank.stop()
                elif command == "c":
                    # print('raw: {}'.format(tcs.read('raw')))
                    rgb = tcs.read('rgb')
                    print("rbg:", rgb)
                    if rgb[0] > 1.5 * rgb[2]:
                        print("Guessed RED")
                        blocks.append(0)
                    else:
                        print("Guessed BLUE")
                        blocks.append(1)
                elif command == "l":
                    actuator.extend_to(0)
                elif command == "p" or command == "d":
                    if command == "p":
                        tank.stop()
                        actuator.extend_to(0.1)
                        sleep(1)
                        servo.slow_set_position(0, 2 / 3)
                        active_block = 1 - active_block
                        #new_scheduled_extra.append(("c", 0))
                    else:
                        tank.stop()
                        actuator.extend_to(0)
                        sleep(5)
                    tank.drive(-v_f)
                    tank.log_sleep(0.7)
                    tank.stop()
                    sleep(0.3)
                    tank.spin(1)
                    tank.log_sleep(1.5)
                    tank.stop()
                    driving = False
                    pos = 0
                    sleep(1.0)
                sleep(0.3)
            tank.drive(v_f)
            if len(new_scheduled_extra) > 0:
                scheduled_extra = new_scheduled_extra
            pos += 1
            if pos == len(path):
                driving = False
                pos = 0
    while True:
        pass
    
if MODE == 2:
    tank.drive(0.6, -0.02)
    for _ in range(50):
        print("pos:", tank.tick(dt))
        sleep(dt)
        
if MODE == 3:
    print("driving mode 3")
    while True:
        print(range_sensor.value())
        sleep(0.5)
