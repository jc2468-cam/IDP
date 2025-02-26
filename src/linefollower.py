#1 left, 1 right, 1 middle sensor. 

while True:
    tank = Sensor()
    left = tank.readleft()
    centre = tank.readcentre()
    right = tank.readright()    
    #0 is white, 1 is black

    if (left == 0 and centre == 1) and right == 0:
        tank.forward()
    elif (left == 0 and centre == 0) and right == 0:
        tank.stop()
    elif (left == 1 and centre == 1) and right == 1:
        tank.stop()
    elif (left == 0 and centre == 0) and right == 0:
        tank.stop()
    elif (left == 1 and centre == 1) and right == 0:
        tank.turnleft()
    elif (left == 1 and centre == 0) and right == 0:
        tank.turnleft()
    elif (left == 0 and centre == 1) and right == 1:
        tank.turnright()
    elif (left == 0 and centre == 0) and right == 1:
        tank.turnright()

    