from math import cos, sin, pi


WHEEL_DIAM = 6.5
AXEL_LENGTH = 20.0

MOTOR_CAL_M = 1.4103222508222688
MOTOR_CAL_C = -0.0991676638734817
MOTOR_CAL_T = 0.3


def discard(board, n=1):
    for o in zip(range(n), board):
        print("discarded", o)
        pass

def read_next(board):
    for (_, out) in zip(range(1), board):
        print("read next", out)
        out = out.strip()
    return out;

def read_nth(board, n):
    for (_, out) in zip(range(n), board):
        print("read nth", out)
        pass
    return out.strip();


class RoboSim:
    def __init__(self):
        self.pos_r = [0,0,0,0]
        self.pos_s = [0,0,0,0]
        self.motion_s = [0,0]
        self.v0, self.v1 = 0, 0

        self.wheel_diam = WHEEL_DIAM
        self.motor_cal_m = MOTOR_CAL_M
        self.motor_cal_c = MOTOR_CAL_C
        self.motor_cal_t = MOTOR_CAL_T
        self.axel_length = AXEL_LENGTH

        self.m0_scale = 1.02
        self.m1_scale = 1.0

        self.wheel_circ = self.wheel_diam * pi
        self.axel_rad = 0.5 * AXEL_LENGTH
    def send_params(self, board):
        board.write(b"Control::load_params({}, {}, {}, {})".format(WHEEL_DIAM, AXEL_LENGTH, MOTOR_CAL_M, MOTOR_CAL_C, MOTOR_CAL_T))
    def fetch_params(self, board):
        board.write(b"Control::fetch_params\r\n")
        reply = read_nth(board, 2)
        if reply[:22] == b"Control::return_params":
            print("Setting params")
            values = [float(v) for v in reply[23:-1].split(b",")]

            self.wheel_diam = values[0]
            self.motor_cal_m = values[1]
            self.motor_cal_c = values[2]
            self.motor_cal_t = values[3]

            self.wheel_circ = self.wheel_diam * pi
            self.axel_factor = 1.0
        else:
            print("Got unexpected reply:", reply)
            raise ValueError
    def predict_pos(self, time):
        radial = (self.motion[1] * time * self.wheel_circ) % pi
        if abs(self.motion[1]) < 1e-3:
            dist = self.motion[0] * self.wheel_circ * time
            theta = self.pos_s[2] + (0.5 * radial)
            dx, dy = dist * cos(theta), dist * sin(theta)
        else:
            motion_rad = self.motion[0] / self.motion[1]
            theta = self.pos_s[2] + radial
            dx, dy = motion_rad * (sin(theta) - sin(self.pos_s[2])), motion_rad * (cos(self.pos_s[2]) - cos(theta))
        self.pos_s[0] += dx
        self.pos_s[1] += dy
        self.pos_s[2] += radial
        self.pos_s[3] += time
    def predict_to_time(self, time):
        self.predict_pos(time - self.pos_s[3])
    def set_reported_pos(self, pos_r):
        self.pos_r = pos_r
    def get_points(self, pos, xc, yc, scale, bot_half_size, bot_facing_len):
        st, ct = sin(pos[2]), cos(pos[2])
        points = list()
        for dx, dy in [(-1,-1), (-1,1), (1,1), (1,-1)]:
            px = xc + int(bot_half_size * (dx * ct - dy * st) + pos[0])
            py = yc - int(bot_half_size * (dx * st + dy * ct) + pos[1])
            points.append((px, py))
        pc = (int(xc + pos[0]), int(yc - pos[1]))
        facing = (int(xc + pos[0] + bot_facing_len * ct), int(yc - pos[1] - bot_facing_len * st))
        return (points, pc, facing)
    def get_reported_points(self, xc, yc, scale, bot_half_size, bot_facing_len):
        return self.get_points(self.pos_r, xc, yc, scale, bot_half_size, bot_facing_len)
    def get_predicted_points(self, xc, yc, scale, bot_half_size, bot_facing_len):
        return self.get_points(self.pos_s, xc, yc, scale, bot_half_size, bot_facing_len)
    def recalculate_motion(self):
        cal_v0 = 0.0 if self.v0 < self.motor_cal_t else self.motor_cal_m * self.v0 + self.motor_cal_c
        cal_v1 = 0.0 if self.v1 < self.motor_cal_t else self.motor_cal_m * self.v1 + self.motor_cal_c
        cal_v_f, cal_v_r = 0.5 * (cal_v0 + cal_v1), (cal_v0 - cal_v1) / self.axel_rad
        self.motion = [cal_v_f, cal_v_r]
    def set_m0_v(self, velocity):
        self.v0 = velocity * self.m0_scale
        self.recalculate_motion()
    def set_m1_v(self, velocity):
        self.v1 = velocity * self.m1_scale
        self.recalculate_motion()
