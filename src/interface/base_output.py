from config import AUTO_HOME, AUTO_HOME_POSITION, MAX_EXTENSION, OUTPUT_MODE
from interface.telemetry_decorator import telemetry_out

from machine import Pin, PWM, Timer


class Motor:
    def __init__(self, m_id, vel_scale=1.0):
        if m_id == 0:
            self.dir_pin = Pin(4, Pin.OUT)
            self.pwm_pin = PWM(Pin(5))
        else:
            self.dir_pin = Pin(7, Pin.OUT)
            self.pwm_pin = PWM(Pin(6))
        self.pwm_pin.freq(1000)
        self.pwm_pin.duty_u16(0)
        self.vel_scale = vel_scale
        self.m_id = m_id
    @telemetry_out(lambda self: f"Motor::off({self.m_id})")
    def off(self):
        self.pwm_pin.duty_u16(0)
    @telemetry_out(lambda self, velocity: f"Motor::run({self.m_id}, {velocity * self.vel_scale})")
    def run(self, velocity):
        if velocity > 0:
            self.dir_pin.value(0)
        else:
            self.dir_pin.value(1)
            velocity = -velocity
        self.pwm_pin.duty_u16(int(65535*velocity*self.vel_scale))

class Led:
    def __init__(self, pin):
        self.pwm_pin = PWM(Pin(pin))
        self.pwm_pin.freq(1000)
        self.state = 0.0
    @telemetry_out(lambda self, b: f"Led::brightness({self.pwm_pin}, {b})", False)
    def brightness(self, b):
        global OUTPUT_MODE
        if OUTPUT_MODE == 0 or OUTPUT_MODE == 2:
            self.pwm_pin.duty_u16(int(65535*b))
        self.state = b
    @telemetry_out(lambda self: f"Led::on({self.pwm_pin})", False)
    def on(self):
        global OUTPUT_MODE
        if OUTPUT_MODE == 0 or OUTPUT_MODE == 2:
            self.pwm_pin.duty_u16(int(65535))
        self.state = 1
    @telemetry_out(lambda self: f"Led::off({self.pwm_pin})", False)
    def off(self):
        global OUTPUT_MODE
        if OUTPUT_MODE == 0 or OUTPUT_MODE == 2:
            self.pwm_pin.duty_u16(int(0))
        self.state = 0
    def toggle(self):
        self.brightness(1 - self.state)
    def blink_ticker(self, frequency):
        def flip_led(f):
            self.toggle()

        timer = Timer()
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=flip_led)

class Actuator:
    def __init__(self, m_id):
        if m_id == 0:
            self.dir_pin = Pin(0, Pin.OUT)
            self.pwm_pin = PWM(Pin(1))
        else:
            self.dir_pin = Pin(3, Pin.OUT)
            self.pwm_pin = PWM(Pin(2))
        self.pwm_pin.freq(1000)
        self.pwm_pin.duty_u16(0)
        self.position = None
        self.runs = 0
        self.m_id = m_id

        if AUTO_HOME:
            self.home(AUTO_HOME_POSITION)
    def set_position(self, position):
        self.position = position
    @telemetry_out(lambda self: f"Actuator::off({self.m_id})")
    def off(self):
        self.pwm_pin.duty_u16(0)
    @telemetry_out(lambda self, velocity=1.0: f"Actuator::extend({self.m_id}, {velocity})")
    def extend(self, velocity=1.0):
        if velocity > 0:
            self.dir_pin.value(0)
        else:
            self.dir_pin.value(1)
            velocity = -velocity
        self.pwm_pin.duty_u16(int(65535*velocity))
    @telemetry_out(lambda self, retract=True, timeout=1000: f"Actuator::home({self.m_id}, {retract})")
    def home(self, retract=True, timeout=8000):
        self.dir_pin.value(1 if retract else 0)
        self.pwm_pin.duty_u16(int(65535))

        def homeing_end(t):
            self.pwm_pin.duty_u16(0)
            self.position = 0 if retract else 1

        timer = Timer()
        timer.init(mode=Timer.ONE_SHOT, period=timeout, callback=homeing_end)
    def extend_to(self, target, rate=1):
        if target > MAX_EXTENSION:
            print("WARNING: Instructed to extend past maximum extension")
            target = MAX_EXTENSION
        full_time = 7800

        if self.position == None:
            raise RuntimeError
        dist = target - self.position

        if dist != 0:
            def extension_end(t):
                self.off()
                self.position = target
                self.runs += 1

            vel = rate if dist > 0 else -1
            timeout = int(abs(dist) * full_time / rate)
            self.extend(vel)

            timer = Timer()
            timer.init(mode=Timer.ONE_SHOT, period=timeout, callback=extension_end)

class Servo:
    def __init__(self, m_id, initial_pos=0):
        self.pwm_pin = PWM(Pin(15 if m_id == 0 else 13))
        self.pwm_pin.freq(50)
        self.m_id = 0
        self.set_position(initial_pos)
    @telemetry_out(lambda self, position: f"Servo::set_position({self.m_id}, {position})")
    def set_position(self, position):
        max_duty = 7864
        min_duty = 1802
        half_duty = int(max_duty/2)
        grad = max_duty - min_duty
        self.pwm_pin.duty_u16(min_duty + int(grad * position))
    def slow_set_position(self, start_pos, position, increments=30, time=5):
        frequency = increments / time
        delta = position - start_pos
        global i
        i = 0

        def advance_position(t):
            global i
            self.set_position(start_pos + (i / increments) * delta)
            i += 1
            if i == increments:
                t.deinit()

        timer = Timer()
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=advance_position)
