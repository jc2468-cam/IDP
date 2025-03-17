from config import *
from machine import I2C
from interface.ranging import *

from interface.interface import *
from interface.base_output import *
from calibrations import *
from interface.linefollowing import LineSensor
from interface.pathing import *

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
    print("Starting simulator input server")
    start_input_sim_monitor()


tank = TrackedTank.default(AXLE_LENGTH, 6.5)
tank.stop()

actuator = Actuator(0)
servo = Servo(0)

#i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
# print(i2c_bus.scan())
#tcs = TCS34725(i2c_bus)

led = Led(28)
led.off()

global MODE


test_location = 0
# position in path list
pos = 0
# position on board
location = "start"

dt = 0.07
v_f = 0.9
button = DigitalInput(8)
MODE = 1
driving = False

def begin(p=0):
    sleep(2.0)
    global MODE
    MODE = 1
    
def stop(p=0):
    global MODE
    MODE = 5

#button.bind_interupt(begin, 1)
while MODE > 4:
    sleep(0.5)

if MODE == 1:
    button.bind_interupt(stop, 1)
    print("driving mode 1")
    sensor1 = DigitalInput(9)
    sensor2 = DigitalInput(10)
    sensor3 = DigitalInput(11)
    sensor4 = DigitalInput(12)
    # list of blocks on the rack
    # -1 for unknown, 0 for red, 1 for blue
    blocks = []
    active_block = 0
    servo_step = 2/3
    ttl = -1
    scheduled_extra = list()
    max_blocks = 2
    
    # weights matrix from floyds, needs updating
    weights = [[0, 284, 389, 52, 300, 0, 0], [304, 0, 179, 336, 188, 0, 0], [320, 179, 0, 347, 40, 0, 0], [52, 316, 357, 0, 332, 0, 0], [300, 168, 111, 332, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    test_path = ["front_house", "factory", "red_drop"]
    #test_path = []
    
    sleep(2)
    
    while True:
        if driving == False:
            print("Location is", location)
            pos = 0
            print("Getting path")
            if len(test_path) > 0:
                if test_location == 0:
                    next_location = "front_house"
                    test_location = 1
                else:
                    location = test_path[test_location - 1]
                    next_location = test_path[test_location]
                    test_location += 1
                if test_location == len(test_path):
                    tank.stop()
                    print("Finished test path")
                    break
                print("Using test path")
                driving = True
            
            else:
                if location == "start":
                    next_location = "front_house"

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

            path = get_path(location, next_location)

            driving = True
            location = next_location

        if driving == True:
            counter = 0
            while sensor1.value() == 0 and sensor4.value() == 0 and counter != ttl and not AUTO_JUNCTION:
                v_r = -0.017 * (sensor2.value() - sensor3.value())
                if LOG_POSITION:
                    print("pos:", tank.tick(dt))
                tank.drive(v_f, v_r)
                sleep(dt)
                counter += 1
            led.on()
            tank.log_sleep(dt)
            new_scheduled_extra = list()
            ttl = -1
            for instruction in path[pos] + scheduled_extra:
                command = instruction[0]
                value = instruction[1]
                print("Junction Detected", command, value)
                if command == "t":
                    tank.log_sleep(0.1)
                    if value > 0:
                        tank.spin(value * 0.9)
                        tank.log_sleep(0.6)
                    if value < 0:
                        tank.spin(value * 0.9)
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
                elif command == "s":
                    ttl = int(value / dt)
                elif command == "p" or command == "d":
                    if command == "p":
                        print("picking")
                        tank.stop()
                        actuator.extend_to(0.15)
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
                    sleep(1.0)
                sleep(0.3)
            tank.drive(v_f)
            if len(new_scheduled_extra) > 0:
                scheduled_extra = new_scheduled_extra
            pos += 1
            if pos == len(path):
                driving = False
    led.off()
    while True:
        pass
    
elif MODE == 2:
    while True:
        sleep(0.1)
        rgb = tcs.read('rgb')
        print("rbg:", rgb)
