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

# position on board
location = "start"

dt = 0.07
v_f = 0.9
button = DigitalInput(8)
MODE = 1


def begin(p=None):
    sleep(2.0)
    global STOP
    STOP = False

def stop(p=None):
    global STOP
    STOP = True


while True:
    full_route_step = 0
    path_step = 0
    STOP = False

    button.bind_interupt(begin, 1)
    while STOP:
        sleep(0.3)
    button.bind_interupt(stop, 1)

    if MODE == 1:
        print("driving mode 1")
        sensor1, sensor2, sensor3, sensor4 = DigitalInput(9), DigitalInput(10), DigitalInput(11), DigitalInput(12)
        # list of blocks on the rack: -1 for unknown, 0 for red, 1 for blue
        blocks, active_block, max_blocks, delivered = [], 0, 2, [0, 0]
        servo_step = 2/3
        scheduled_extra = list()
        ttl = -1
        driving = False

        full_route = ["front_house", "factory", "back_house", "warehouse", "start"]

        while True:
            if not driving:
                print("Location is", location)
                path_step = 0

                if len(blocks) == max_blocks or (len(blocks) != 0 and full_route_step == len(full_route)):
                    if 0 in blocks:
                        next_location = "red_drop"
                        if blocks[active_block] != 0:
                            counter = 0
                            for b in blocks:
                                if b != 0:
                                    counter += 1
                                else:
                                    break
                            servo.slow_set_position(servo_step * counter)
                            active_block = counter
                    else:
                        next_location = "blue_drop"
                else:
                    if full_route_step == len(full_route):
                        if location == "start":
                            break
                        else:
                            next_location = "start"
                    next_location = full_route[full_route_step]
                    full_route_step += 1

                print("Pathing to", next_location)
                path = get_path(location, next_location)

                driving = True
                location = next_location
            else:
                if STOP:
                    break
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
                for instruction in path[path_step] + scheduled_extra:
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
                        # rgb = tcs.read('rgb')
                        rgb = (123.2, 13.7, 19.2) if delivered[0] != 2 else (100.1, 100.1, 100.1)
                        print("rbg:", rgb)
                        if rgb[0] > 1.5 * rgb[2]:
                            print("Guessed RED")
                            blocks[-1] = 0
                        else:
                            print("Guessed BLUE")
                            blocks[-1] = 1
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
                            blocks.append(-1)
                            active_block = (active_block + 1) % max_blocks
                            servo.slow_set_position(servo_step * len(blocks))
                            new_scheduled_extra.append(("c", 0))
                        else:
                            target_id = 0 if location == "red_drop" else 1
                            t0, tr, initial = 2, 1, True
                            while target_id in blocks:
                                if initial:
                                    print("Dropping first block")
                                    t_forward = t0 - (tr * delivered[target_id])
                                    tank.drive(v_f)
                                    tank.log_sleep(t_forward)
                                    tank.stop()
                                    blocks[active_block] = None
                                    initial = False
                                else:
                                    print("Dropping subsequent block")
                                    tank.drive(-v_f)
                                    tank.log_sleep(tr)
                                    tank.stop()
                                    actuator.extend_to(0.1)
                                    counter = 0
                                    for b in blocks:
                                        if b != target_id:
                                            counter += 1
                                        else:
                                            break
                                    servo.slow_set_position(servo_step * counter)
                                    blocks[counter] = None
                                    sleep(5)
                                actuator.extend_to(0)
                                delivered[target_id] += 1
                                sleep(1)
                            blocks = list()
                        tank.drive(-v_f)
                        tank.log_sleep(0.7)
                        tank.stop()
                        sleep(0.3)
                        tank.spin(1)
                        tank.log_sleep(1.5)
                        tank.stop()
                        if command == "d":
                            servo.set_position(0)
                            active_block = 0
                    sleep(0.3)
                tank.drive(v_f)
                scheduled_extra = new_scheduled_extra
                path_step += 1
                if path_step == len(path):
                    driving = False
        tank.stop()
        led.off()
        print("Finished full route")
    elif MODE == 2:
        while True:
            sleep(0.1)
            rgb = tcs.read('rgb')
            print("rbg:", rgb)
