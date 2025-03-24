global OUTPUT_MODE, INPUT_MODE, AWAIT_LINK
# 0: physical only    1: telemetry only    2: both
OUTPUT_MODE = 0
# 0: physical only    1: telemetry only    2: both
INPUT_MODE = 0
# Wait for host to indicate link before starting.
AWAIT_LINK = False

global WHEEL_DIAM, AXLE_LENGTH
# Diameter of drive wheels, in cm.
WHEEL_DIAM = 6.5
# Distance between drive wheels, in cm.
AXLE_LENGTH = 20.0

global MOTOR_CAL_M, MOTOR_CAL_C, MOTOR_CAL_T
# Linearity constant of motor speed, in Hz / full duty.
MOTOR_CAL_M = 1.4103222508222688
# Offset of motor speed, in Hz.
MOTOR_CAL_C = -0.0991676638734817
# Motor minimum power threshold, in duty cycle.
MOTOR_CAL_T = 0.3

# Whether to automatically home actuators when they are initialized.
AUTO_HOME = True
# If actuators are automatically homes, whether to home them to the retracted position (otherwise extended position is used).
AUTO_HOME_POSITION = True
# How long an actuator can wait for homing to complete when `extend_to` is called, before raising an exception.
AWAIT_HOMING = 10.0
# The maximum position an actuator can be told to extend to using `extend_to`.
MAX_EXTENSION = 0.15

# Whether to shake servo in main loop to improve reliability.
SHAKE_SERVO = True

# Force junction instructions to be triggered automatically in order, used for testing.
AUTO_JUNCTION = False

# Whether to output robot position over serial for telemetry.
LOG_POSITION = False
