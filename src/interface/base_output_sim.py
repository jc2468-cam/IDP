# Equivalent to base_output.py, but logs all instructions to the console instead of actually executing them.

# from machine import Timer


class Motor:
    def __init__(self, m_id, vel_scale=1.0):
        self.m_id = m_id
        self.vel_scale = vel_scale
    def off(self):
        print(f"Motor::off({self.m_id})")
    def run(self, velocity):
        print(f"Motor::run({self.m_id}, {velocity * self.vel_scale})")

class Led:
    def __init__(self, pin):
        self.pwm_pin = pin
        self.state = 0.0
    def brightness(self, b):
        print(f"Led::brightness({self.pwm_pin}, {b})")
        self.state = b
    def on(self):
        print(f"Led::on({self.pwm_pin})")
        self.state = 1
    def off(self):
        print(f"Led::off({self.pwm_pin})")
        self.state = 0
    def toggle(self):
        self.brightness(1 - self.state)
    # def blink_ticker(self, frequency):
    #     def flip_led(f):
    #         self.toggle()

    #     timer = Timer()
    #     timer.init(freq=frequency, mode=Timer.PERIODIC, callback=flip_led)
    def blink_ticker(self, frequency):
        raise RuntimeError
