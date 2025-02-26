from interface import *
from calibrations import *

class Map:
    def __init__(self):
        self.pathToBlue = []
        self.pathToRed = []
        self.pathToGreen = []
        self.pathToYellow = []
        self.pathToRY = []
        self.pathToGB = []

    


def create_instructions():
    pass

def path(instructions):
    tank = TrackedTank(m1,m2,axel_len,wheel_di)
    #instructions = [[vf0,vr0,time0], [vf1, vr1, time1], etc.]
    for i in instructions:
        if i.length() == 3:
            tank.drive(instructions[i][0], instructions[i][1], instructions[i][2])
        else:
            tank.pickup()
        tank.stop()
    
    
    


