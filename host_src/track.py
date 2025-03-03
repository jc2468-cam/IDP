import numpy as np
import pygame
import serial


board = serial.Serial("COM4", 115200, timeout=10)


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

# board = [b"pos: [100.4, 200.4, 0.1, 10.6]"] * 10000

exit = False
for l in board:
    if l[:3] == b"pos":
        pos = [float(v) * scale for v in l[5:].strip()[1:-1].split(b",")]
        # print([round(x, 2) for x in pos])
        canvas.fill((0,0,0))
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
        if exit:
            break

        st, ct = np.sin(pos[2]), np.cos(pos[2])
        points = list()
        for dx, dy in [(-1,-1), (-1,1), (1,1), (1,-1)]:
            px = xc + int(bot_half_size * (dx * ct - dy * st) + pos[0])
            py = yc - int(bot_half_size * (dx * st + dy * ct) + pos[1])
            points.append((px, py))
        pc = (int(xc + pos[0]), int(yc - pos[1]))
        facing = (int(xc + pos[0] + bot_facing_len * ct), int(yc - pos[1] - bot_facing_len * st))
        for l in env_lines:
            pygame.draw.line(canvas, (255,255,255), *[env_points[p] for p in l])
        pygame.draw.polygon(canvas, (0,255,0), points)
        pygame.draw.line(canvas, (0,0,255), pc, facing)
        pygame.draw.rect(canvas, (255,0,0), pygame.Rect(xc-5,yc-5,10,10))
        pygame.display.update()
