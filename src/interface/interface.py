from config import *

from interface.base_output import *
from interface.base_input import *

from math import cos, sin, pi
from utime import sleep


class Tank:
    """A 2 driven wheel 'tank drive' configuration.

    See `TrackedTank`"""
    def __init__(self, m0, m1, axle_length):
        self.m0 = m0
        self.m1 = m1
        self.axle_rad = axle_length * 0.5
    def default(axle_length, vel_scale=1.0):
        return Tank(Motor(0, vel_scale), Motor(1, vel_scale), axle_length)
    def drive(self, v_f, v_r=0.0):
        self.run_raw(*self.get_motor_speeds(v_f, v_r))
    def spin(self, v):
        self.run_raw(v, -v)
    def stop(self):
        self.m0.off()
        self.m1.off()
    def get_motor_speeds(self, v_f, v_r=0.0):
        diff_vel = v_r * self.axle_rad
        v0, v1 = v_f + diff_vel, v_f - diff_vel
        limit = max(abs(v0), abs(v1))
        if limit > 1.0:
            v0 /= limit
            v1 /= limit
        return (v0, v1)
    def run_raw(self, v0, v1):
        self.m0.run(v0)
        self.m1.run(v1)


class TrackedTank:
    """A 2 driven wheel 'tank drive' configuration.

    Tracks the estimated position of the robot using dead reckoning and calibration data for the motors (provided in the config file).
    """
    def __init__(self, m0, m1, axle_length, wheel_diam):
        """Creates a new `TrackedTank` from the driving motors.

        Arguments:
            `m0` (`Motor`): The left motor of the tank drive.
            `m1` (`Motor`): The right motor of the tank drive.
            `axle_length` (`float`): The distance between the two drive wheels.
            `wheel_diam` (`float`): The diameter of the driving wheels.

        Returns:
            `TrankedTank`: The created tank drive.
        """
        self.inner = Tank(m0, m1, axle_length)
        self.pos = [0,0,0,0]
        self.motion = [0, 0]
        self.wheel_circ = wheel_diam * pi
    def default(axle_length, wheel_diam, vel_scale=1.0):
        """Creates a new `TrackedTank`, creating the motors with default configurations (and a specified velocity scaling).

        Arguments:
            `axle_length` (`float`): The distance between the two drive wheels.
            `wheel_diam` (`float`): The diameter of the driving wheels.
            `vel_scale` (`float`): A scaling factor for the velocity of the tank drive (default `1.0` - no scaling).

        Returns:
            `TrankedTank`: The created tank drive.
        """
        return TrackedTank(Motor(0, vel_scale), Motor(1, vel_scale), axle_length, wheel_diam)
    def update_motion(self, v0, v1):
        """Calculates the motion of the tank drive based on the power each motor is being driven at.

        Arguments:
            `v0` (`float`): The driving power of the left motor.
            `v1` (`float`): The driving power of the right motor.
        """
        cal_v0 = 0.0 if abs(v0) < MOTOR_CAL_T else MOTOR_CAL_M * v0 + MOTOR_CAL_C
        cal_v1 = 0.0 if abs(v1) < MOTOR_CAL_T else MOTOR_CAL_M * v1 + MOTOR_CAL_C
        cal_v_f, cal_v_r = 0.5 * (cal_v0 + cal_v1), 0.5 * (cal_v0 - cal_v1) / self.inner.axle_rad
        self.motion = [cal_v_f, cal_v_r]
    def drive(self, v_f, v_r=0.0, t=0.0):
        """Drives the tank with a specified power forward and a specified rotation rate.

        Arguments:
            `v_f` (`float`): The power at which to drive forward. This will nominally be the average power of the 2 motors, but if one of the
                motors would exceed maximum drive power the power to both is scaled to keep the correct ratio.
            `v_r` (`float`): The rate at which to turn the tank drive (positive anti-clockwise). The turning rate is given (nominally) in radians per time taken
                to drive 1 cm at full power.
            `t` (`float`): Allows the tracking position to be automatically updated with a given drive time, useful for calling drive in a loop (optional).
        """
        if t != 0:
            self.tick(t)
        v0, v1 = self.inner.get_motor_speeds(v_f, v_r)
        self.update_motion(v0, v1)
        self.inner.run_raw(v0, v1)
    def spin(self, v):
        """Rotates the robot in place.

        Arguments:
            `v` (`float`): The power at which to spin (range [-1 - 1], positive anti-clockwise).
        """
        self.update_motion(v, -v)
        self.inner.run_raw(v, -v)
    def stop(self):
        """Stops the tank drive in place."""
        self.inner.stop()
        self.motion = [0, 0]
    def tick(self, time):
        """Updates the calculated position of the tank drive based on dead reckoning.

        The position is updated using arcs about a calculated centre of rotation rather than linear segments to allow larger times between updates without loosing precision.

        Arguments:
            `time` (`float`): The time the tank drive has been driving for since the last tick, in seconds.
        """
        radial = (self.motion[1] * time * self.wheel_circ) % pi
        if self.motion[1] < 0:
            radial -= pi
        if abs(self.motion[1]) < 1e-3:
            dist = self.motion[0] * self.wheel_circ * time
            theta = self.pos[2] + (0.5 * radial)
            dx, dy = dist * cos(theta), dist * sin(theta)
        else:
            motion_rad = self.motion[0] / self.motion[1]
            theta = self.pos[2] + radial
            dx, dy = motion_rad * (sin(theta) - sin(self.pos[2])), motion_rad * (cos(self.pos[2]) - cos(theta))
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += radial
        self.pos[3] += time
        return self.pos
    def log_tick(self, time):
        """Updates the calculated position of the tank drive, and outputs it over serial to a host computer for telemetry if configured in the config file.

        See `tick`
        """
        if LOG_POSITION:
            print("pos:", self.tick(time))
    def log_sleep(self, time):
        """Sleeps a specified time (in seconds), then updates the calculated position, and outputs it over serial if configured.

        See `log_tick`"""
        sleep(time)
        self.log_tick(time)
    def last_pos(self):
        """Returns the last calculated position of the tank drive in the format:
        (
            `x`: The x (forward) position, in cm,
            `y`: The y (lateral, positive right) position, in cm,
            `theta`: The facing direction relative to the initial heading, positive anti-clockwise, in radians,
            `time`: The time at which the position was last updated, in seconds since the first motion function (`drive` / `stop`) call, in seconds,
        )
        """
        return self.pos

def timer_queue(commands):
    """Executes a list of functions with delays between them, without blocking.

    This function uses hardware timer callbacks to schedule the tasks.

    Arguments:
        `commands` (`list`): Pairs of `(callback, time_to_next_command)` groups to be excluded in order, `time_to_next_command` given in seconds.
    """
    callbacks = list()
    for (i, command) in commands[:-1]:
        def inner(t):
            command[0]()
            t.init(mode=Timer.ONE_SHOT, period=int(command[1] * 1000), callback=callbacks[i+1])
        callbacks.append(inner)
    callbacks.append(commands[-1][0])
