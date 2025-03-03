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
    def off(self):
        self.pwm_pin.duty_u16(0)
    def run(self, velocity):
        if velocity > 0:
            self.dir_pin.value(0)
        else:
            self.dir_pin.value(1)
            velocity += 1
        self.pwm_pin.duty_u16(int(65535*velocity*self.vel_scale))

class Led:
    def __init__(self, pin):
        self.pwm_pin = PWM(Pin(pin))
        self.pwm_pin.freq(1000)
        self.state = 0.0
    def brightness(self, b):
        self.pwm_pin.duty_u16(int(65535*b))
        self.state = b
    def on(self):
        self.pwm_pin.duty_u16(int(65535))
        self.state = 1
    def off(self):
        self.pwm_pin.duty_u16(int(0))
        self.state = 0
    def toggle(self):
        self.brightness(1 - self.state)
    def blink_ticker(self, frequency):
        def flip_led(f):
            self.toggle()

        timer = Timer()
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=flip_led)
