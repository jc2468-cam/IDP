from sim import RoboSim, discard, read_next, read_nth

import numpy as np
import pygame
import serial


board = serial.Serial("COM5", 115200, timeout=4)


env_points = [(0,0), (30,0), (30,100), (30,-100)]
env_lines = [(0,1), (1,2), (1,3)]

screen_size = (750, 750)
xc, yc = (screen_size[0] // 2), (screen_size[1] // 2)
scale = 1.0
bot_half_size = 10
bot_facing_len = 75

for (i, p) in enumerate(env_points):
    env_points[i] = (p[0] + xc, p[1] + yc)


pygame.init()
canvas = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Track Bot")


bot = RoboSim()

discard(board)
board.write(b"Control::start\r\n")
discard(board)
bot.fetch_params(board)

counter = 0
exit = False
redraw = False
for l in board:
    l = l.strip()
    redraw = False
    if l[:7] == b"Motor::":
        if l[7:10] == b"run":
            m_id, vel = [float(v) for v in l[11:-1].split(b",")]
            if m_id == 0:
                bot.set_m0_v(vel)
            else:
                bot.set_m1_v(vel)
    elif l[:3] == b"pos":
        pos_r = [float(v) * scale for v in l[6:-1].split(b",")]
        # print([round(x, 2) for x in pos_r])
        bot.set_reported_pos(pos_r)
        bot.predict_to_time(pos_r[3])
        redraw = True
    else:
        print("MSG:", l)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    if exit:
        break

    if redraw:
        canvas.fill((0,0,0))
        points_r, pc_r, facing_r = bot.get_reported_points(xc, yc, scale, bot_half_size, bot_facing_len)
        points_s, pc_s, facing_s = bot.get_predicted_points(xc, yc, scale, int(bot_half_size * 0.6), int(bot_facing_len * 0.6))

        for l in env_lines:
            pygame.draw.line(canvas, (255,255,255), *[env_points[p] for p in l])
        pygame.draw.polygon(canvas, (0,255,0), points_r)
        pygame.draw.line(canvas, (0,0,255), pc_r, facing_r)
        pygame.draw.polygon(canvas, (255,255,0), points_s)
        pygame.draw.line(canvas, (0,128,255), pc_s, facing_s)
        pygame.draw.rect(canvas, (255,0,0), pygame.Rect(xc-5,yc-5,10,10))
        pygame.display.update()

        counter += 1
        if counter == 10:
            board.write(b"~\r\n")
            discard(board)
            board.write(b"Control::set_pin(9,1)\r\n")
            discard(board)
        if counter == 11:
            board.write(b"~\r\n")
            discard(board)
            board.write(b"Control::set_pin(9,0)\r\n")
            discard(board)
