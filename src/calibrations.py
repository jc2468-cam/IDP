from utime import sleep, ticks_ms
from machine import Pin

def straight_line(tank, t=10, v=1.0):
    tank.drive(v)
    sleep(t)
    tank.stop()

def spin(tank, t=10, v=1.0):
    tank.drive(0.0, v)
    sleep(t)
    tank.stop()

def motor_stepped_ramp(motor, steps=10, t=10, v_max=1.0):
    for s in range(steps):
        motor.run(s * v_max / steps)
        sleep(t / steps)
    motor.off()

def blink_led(led, rate=1.0, t=10):
    for _ in range(rate * t):
        led.on()
        sleep(0.5 / rate)
        led.off()
        sleep(0.5 / rate)

def motor_tacho(motor, sensor_pin, steps=5, v_step=0.1, v_start=0.2, v_max=1):
    global times, counter, speed
    
    speed = v_start
    motor.off()

    def log_sensor(p):
        global times, counter, speed
        times.append(ticks_ms())
        counter += 1
        if counter == steps:
            counter = 0
            print(times)
            speed_str = str(round(speed, 3)).replace(".", "_")
            with open(f"out_{speed_str}.txt", "w") as f:
                f.write(str(times))
            times = list()
            if speed < v_max:
                speed += v_step
                motor.run(speed)
            else:
                motor.off()
    
    times = list()
    counter = 0
    sensor_pin.irq(log_sensor, Pin.IRQ_RISING)
    
    sleep(5)
    motor.run(speed)

