from config import AUTO_HOME, AUTO_HOME_POSITION, MAX_EXTENSION, AWAIT_HOMING, OUTPUT_MODE
from interface.telemetry_decorator import telemetry_out

from machine import Pin, PWM, Timer
from utime import sleep


class Motor:
    """A PWM controlled DC motor."""
    def __init__(self, m_id, vel_scale=1.0):
        """Creates a new `Motor`.

        Arguments:
            `m_id` (`int`): Which channel of the motor controller to use (`0` or `1`).
            `vel_scale` (`float`): Allows a scaling factor to be applied to the velocity of the motor.

        Returns:
            `Motor`: The created motor.
        """
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
        """Cuts power to the motor."""
        self.pwm_pin.duty_u16(0)
    @telemetry_out(lambda self, velocity: f"Motor::run({self.m_id}, {velocity * self.vel_scale})")
    def run(self, velocity):
        """Runs the motor at a specified power level.

        The velocity of the IDP motors is approximately linear with PWM duty cycle.

        Arguments:
            `velocity` (`float`): The PWM duty cycle to run the motor at (uses negative velocities to run the motor backwards).
        """
        if velocity > 0:
            self.dir_pin.value(0)
        else:
            self.dir_pin.value(1)
            velocity = -velocity
        self.pwm_pin.duty_u16(int(65535*velocity*self.vel_scale))

class Led:
    """Represents an output pin connected to an LED.

    Allows PWM control of the brightness, toggling the LED, and blinking the LED in software (only used during testing).
    """
    def __init__(self, pin):
        """Creates a new `LED`

        Arguments:
            `pin_id` (`int`): The GPIO pin number the LED is connected to.
        """
        self.pwm_pin = PWM(Pin(pin))
        self.pwm_pin.freq(1000)
        self.state = 0.0
    @telemetry_out(lambda self, b: f"Led::brightness({self.pwm_pin}, {b})", False)
    def brightness(self, b):
        """Sets the brightness of the LED using PWM.

        Arguments:
            `b` (`float`): The brightness of the LED (range [0-1]).
        """
        global OUTPUT_MODE
        if OUTPUT_MODE == 0 or OUTPUT_MODE == 2:
            self.pwm_pin.duty_u16(int(65535*b))
        self.state = b
    @telemetry_out(lambda self: f"Led::on({self.pwm_pin})", False)
    def on(self):
        """Sets the LED to fully on."""
        global OUTPUT_MODE
        if OUTPUT_MODE == 0 or OUTPUT_MODE == 2:
            self.pwm_pin.duty_u16(int(65535))
        self.state = 1
    @telemetry_out(lambda self: f"Led::off({self.pwm_pin})", False)
    def off(self):
        """Sets the LED to fully off."""
        global OUTPUT_MODE
        if OUTPUT_MODE == 0 or OUTPUT_MODE == 2:
            self.pwm_pin.duty_u16(int(0))
        self.state = 0
    def toggle(self):
        """Inverts the brightness of the LED."""
        self.brightness(1 - self.state)
    def blink_ticker(self, frequency):
        """Blinks the LED periodically in software. Only used during testing."""
        def flip_led(f):
            self.toggle()

        timer = Timer()
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=flip_led)

class Actuator:
    """A linear actuator.

    Uses timing to track the position of the actuator, and allows soft limits to be configured in the config file.
    """
    def __init__(self, m_id):
        """Creates a new `Actuator`.

        If it is configured in the config file, the actuator will be automatically homed when it is created.

        Arguments:
            `m_id` (`int`): Which channel of the actuator controller to use (`0` or `1`).

        Returns:
            `Actuator`: The created actuator.
        """
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
        """Sets the internal tracking position of the actuator."""
        self.position = position
    @telemetry_out(lambda self: f"Actuator::off({self.m_id})")
    def off(self):
        """Stops extending / retracting the actuator."""
        self.pwm_pin.duty_u16(0)
    @telemetry_out(lambda self, velocity=1.0: f"Actuator::extend({self.m_id}, {velocity})")
    def extend(self, velocity=1.0):
        """Extends / retracts the actuator.

        Arguments:
            `velocity` (`float`): The rate at which to extend the actuator (uses negative velocities to retract the actuator).
        """
        if velocity > 0:
            self.dir_pin.value(0)
        else:
            self.dir_pin.value(1)
            velocity = -velocity
        self.pwm_pin.duty_u16(int(65535*velocity))
    @telemetry_out(lambda self, retract=True, timeout=1000: f"Actuator::home({self.m_id}, {retract})")
    def home(self, retract=True, timeout=8000):
        """Extends the actuator up to one of its internal limit switches, and sets the now known position of the actuator for tracking.

        The actuator will not allow tracking of its position until `home` in called, or the position is specified by the user using `set_position`.
        This is because the actuator does not have any encoder, so when the robot is powered up the position of the actuator is initially not known.

        Arguments:
            `retract` (`bool`): Whether to home the actuator to the fully retracted (default) or extended position.
            `timeout` (`int`): The maximum number of milliseconds to wait for to ensure homing is completed.
        """
        self.dir_pin.value(1 if retract else 0)
        self.pwm_pin.duty_u16(int(65535))

        def homeing_end(t):
            self.pwm_pin.duty_u16(0)
            self.position = 0 if retract else 1

        timer = Timer()
        timer.init(mode=Timer.ONE_SHOT, period=timeout, callback=homeing_end)
    def extend_to(self, target, rate=1):
        """Extends the actuator to a specified position using the internal tracked position and timing.

        This can only used once the actuator has been homed (see `home`), or the user has specified the actuator position. If the actuator has
        not been homed, this function will either wait for it to be homed (up to a maximum delay), or raise an exception depending on the config file.

        This function will only allow the actuator to extend up to the limit set in the config file, and will give a warning if an out-of-range value is given.

        Arguments:
            `target` (`float`): The position to set the actuator to (range [0, 1]).
            `rate` (`float`): The rate at which to extend / retract the actuator (default full speed).
        """
        if target > MAX_EXTENSION:
            print("WARNING: Instructed to extend past maximum extension")
            target = MAX_EXTENSION
        full_time = 7800

        if self.position == None:
            homing_failed = True
            if AWAIT_HOMING != None:
                dt = 0.5
                for _ in range(int(AWAIT_HOMING / dt)):
                    sleep(dt)
                    if self.position != None:
                        homing_failed = False
                        break
            if homing_failed:
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
    """Represents a servo motor."""
    def __init__(self, m_id, initial_pos=0.0):
        """Creates a new `Servo`, and sets its initial position.

        Arguments:
            `m_id` (`int`): Which channel of the servo driver to use (`0` or `1`).
            `initial_pos` (`float`): The initial position to set the servo to.
        Returns:
            `Servo`: The created servo.
        """
        self.pwm_pin = PWM(Pin(15 if m_id == 0 else 13))
        self.pwm_pin.freq(50)
        self.m_id = 0
        self.spinning = False
        self.set_position(initial_pos)
    @telemetry_out(lambda self, position: f"Servo::set_position({self.m_id}, {position})")
    def set_position(self, position):
        """ Sets the servo to the specified position at maximum speed.

        Arguments:
            `position` (`float`): The target position of the servo (range [0 - 1]).
        """
        max_duty = 7864
        min_duty = 1802
        half_duty = int(max_duty/2)
        grad = max_duty - min_duty
        self.pwm_pin.duty_u16(min_duty + int(grad * position))
        self.position = position
    def slow_set_position(self, target_position, increments=30, time=2.0):
        """Slowly sets the position of the servo by moving in small increments over an extended time.

        Arguments:
            `target_position` (`float`): The target position of the servo (range [0 - 1]).
            `increments` (`int`): The number of steps to move the servo over (default `30`).
            `time` (`float`): The number of seconds over which to move the servo (default `2.0`).
        """
        frequency = increments / time
        start_position = self.position
        delta = target_position - start_position
        global slow_set_i
        slow_set_i = 0

        def advance_position(t):
            global slow_set_i
            if slow_set_i < increments:
                self.set_position(start_position + (slow_set_i / increments) * delta)
                slow_set_i += 1
            else:
                self.set_position(target_position)
                self.spinning = False
                t.deinit()

        timer = Timer()
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=advance_position)
        self.spinning = True
    def await_spinning(self, dt=0.2):
        """Wait until all pending actions (slow spinning or shaking) have completed.

        Arguments:
            `dt` (`float`): How often to check whether the servo is complete in seconds (default `0.2`).
        """
        while self.spinning:
            sleep(dt)
    def shake(self, ampliude=0.075, frequency=4, time=1.0):
        """Shake the servo back and forth around its current position.

        Arguments:
            `amplitude` (`float`): The fraction of the servo's range over which to shake.
            `frequency` (`float`): The frequency at which to shake the servo (in Hz).
            `time` (`float`): How many seconds to shake the servo for.
        """
        initial_position = self.position
        shake_steps = int(time / freq)
        global shake_i
        shake_i = 0

        def shake_step(t):
            global shake_i
            if shake_i < shake_steps:
                self.set_position(self.position + ampliude if (shake_i & 1) == 0 else -ampliude)
                shake_i += 1
            else:
                self.set_position(initial_position)
                self.spinning = False
                t.deinit()

        timer = Timer()
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=shake_step)
        self.spinning = True
