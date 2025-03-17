global OUTPUT_MODE, INPUT_MODE, AWAIT_LINK
# 0: physical only    1: telemetry only    2: both
OUTPUT_MODE = 0
# 0: physical only    1: telemetry only    2: both
INPUT_MODE = 0
# wait for host to indicate link before starting
AWAIT_LINK = False

global WHEEL_DIAM, AXLE_LENGTH
WHEEL_DIAM = 6.5
AXLE_LENGTH = 20.0

global MOTOR_CAL_M, MOTOR_CAL_C, MOTOR_CAL_T
MOTOR_CAL_M = 1.4103222508222688
MOTOR_CAL_C = -0.0991676638734817
MOTOR_CAL_T = 0.3

AUTO_HOME = True
AUTO_HOME_POSITION = True
AWAIT_HOMING = 10.0
MAX_EXTENSION = 0.15

AUTO_JUNCTION = True

LOG_POSITION = False
