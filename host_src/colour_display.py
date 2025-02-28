import pygame
import serial


board = serial.Serial("COM4", 115200, timeout=10)


pygame.init()

canvas = pygame.display.set_mode((500,500))

pygame.display.set_caption("Show Colour")

adj = 3.

exit = False
for (i, l) in zip(range(10000), board):
    if l[:3] == b"rgb":
        col = [min(float(v) * adj, 255) for v in l[5:].strip()[1:-1].split(b",")]
        print([round(x, 2) for x in col])
        canvas.fill(col)
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
        if exit:
            break
        pygame.display.update()
