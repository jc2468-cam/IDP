from utime import sleep

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
