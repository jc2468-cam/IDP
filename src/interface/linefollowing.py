from .base_input import DigitalInput
from machine import Timer
from .interface import Tank, TrackedTank

class LineSensor:
    
    """class containing the 4 line sensors and relevant functions"""
    # define the sensors as pin inputs
    def __init__(self, tank, sensor_1_pin, sensor_2_pin, sensor_3_pin, sensor_4_pin):
        self.sensor1 = DigitalInput(sensor_1_pin)
        self.sensor2 = DigitalInput(sensor_2_pin)
        self.sensor3 = DigitalInput(sensor_3_pin)
        self.sensor4 = DigitalInput(sensor_4_pin)
        
        # tank must be a tank object. raise objection if not
        self.tank = tank
        if type(tank) != TrackedTank and type(tank) != Tank:
            raise TypeError("tank parameter must be a tank object")
            
        self.integral = 0
        self.x_values = [0]
        
    """def tick(self):
        print("sensor 1: ", self.sensor1.value())
        print("sensor 2: ", self.sensor2.value())
        print("sensor 3: ", self.sensor3.value())
        print("sensor 4: ", self.sensor4.value())"""
    
    def line_follow(self, v_f, time_interval):
        """uses the line sensors and drives the tank forward at speed v_f"""
        
        def tick(p=0):
            print("sensor 1: ", self.sensor1.value())
            print("sensor 2: ", self.sensor2.value())
            print("sensor 3: ", self.sensor3.value())
            print("sensor 4: ", self.sensor4.value())
        
        def control_function(self):
            # weighting for the sensors
            x = self.sensor1.value() * 2 + self.sensor2.value() - self.sensor3.value() - self.sensor4.value() * 2
            self.x_values.append(x)
            
            # PID controller
            kp = 0.02
            kd = 0
            ki = 0
            x_diff = self.x_values[-1] - self.x_values[-2]           
            result = kp * x + kd * x_diff + ki * self.integral
            return result

        # create a list of bend positions and see which one you're closest to.
        # format: (x, y, approach direction)
        # x left and right from origin, y away from origin (towards building)
        # approach directions: compass directions
        self.bend_positions = ((0, 0), # 0
                               (0, 31),
                               (0, 31),
                               (0, 31),
                               (0, 31),
                               (104, 31), # 5
                               (104, 31),
                               (104, 31),
                               (104, 31),
                               (-104, 31),
                               (-104, 31), # 10
                               (-104, 31),
                               (-104, 31),
                               (-104, 115),
                               (-104, 115),
                               (-104, 115), # 15
                               (-104, 115),
                               (-104, 193),
                               (-104, 193),
                               (-104, 193),
                               (-104, 193), # 20
                               (0, 193),
                               (0, 193),
                               (0, 193),
                               (0, 193),
                               (104, 193), # 25
                               (104, 193),
                               (104, 193),
                               (104, 193)
                               (104, 115),
                               (104, 115), # 30
                               (104, 115),
                               (104, 115),
                               (0, 115),
                               (0, 115),
                               (0, 115), # 35
                               (0, 115),
                               (-32, 31),
                               (-32, 31),
                               (-32, 31),
                               (-32, 31), # 40
                               (34, 115),
                               (34, 115),
                               (34, 115),
                               (34, 115),
                               (0, 152), # 45
                               (0, 152),
                               (0, 152),
                               (0, 152),
                               (42, 193),
                               (42, 193), # 50
                               (42, 193),
                               (42, 193),)
        
        def compass_pointify(points):
            result = []
            n = 2
            for point in points:
                result.append((point[1], point[0] (3.14/2)*(n%4)))
                n += 1
            return tuple(result)
        
        self.bend_positions = compass_pointify(self.bend_positions)
        print(self.bend_positions)
        self.bend_initiate = False
        self.bending = False
        
        def integrate(p=None):
            
            def unbend(p=None):
                self.bending = False
            
            # check for bend
            if self.bend_initiate == True:
                if (self.sensor1.value() == 1 and self.sensor2.value() == 1) or (self.sensor3.value() == 1 and self.sensor4.value() == 1):
                    
                    # find rotation
                    rotation = (self.pos[3] * 18 / 3.14)%36
                    if rotation < 4.5:
                        rotation = 0
                    if 4.5 < rotation and rotation < 13.5:
                        rotation = 27
                    if 13.5 < rotation:
                        rotation = 18   
                    if -4.5 < rotation:
                        rotation = 0
                    if -13.5 < rotation and rotation < -4.5:
                        rotation = 9
                    if -13.5 > rotation:
                        rotation = 18   
                    print("rotation = ", rotation)            
                    self.pos = self.tank.last_pos()
                    bend_x = self.bend_positions[1] - self.pos[1]
                    bend_y = self.bend_positions[0] - self.pos[0]
                    bend_divergence = bend_x + bend_y
                    node_number = bend_divergence.index(min(bend_divergence))
                    bend_shell = self.bend_positions[node_number]
                    bend = (bend_shell[0], bend_shell[1], rotation)
                    print("bend ", bend)
                    node_number = self.bend_positions.index(bend)
                    print("node number = ", node_number)
                    # do Floyd on node number
                    # next node will only be in a cardinal direction from current
                    next_node = 2
                    next_rotation = self.bend_positions[next_node][2]
                    # if next_node[0] == bend[0]:
                    #     if next_node[1] > bend[1]:
                    #         next_rotation = 9
                    #         pass  
                    #     if next_node[1] < bend [1]:
                    #         next_rotation = 27
                    #         pass
                    # if next_node[1] == bend[1]:
                    #     if next_node[0] > bend[0]:
                    #         next_rotation = 0
                    #         pass  
                    #     if next_node[0] < bend [0]:
                    #         next_rotation = 18
                    #         pass
                        
                    rotation_needed = rotation - next_rotation  
                    v_r_in = 0.2
                    rotation_time = rotation_needed / v_r_in                
                    self.tank.drive(0, v_r = v_r_in, t = rotation_time)
                    self.bend_initiate = False
                    timer3 = Timer()
                    timer3.init(freq=(1/rotation_time), mode=Timer.ONESHOT, callback=unbend)               
            
            # else just line follow
            if self.bending == False:
                #print("integrating")
                self.integral += control_function(self) * time_interval
                self.tank.drive(v_f, control_function(self))
        
        timer = Timer()
        timer.init(freq=(1/time_interval), mode=Timer.PERIODIC, callback=integrate)  
        timer2 = Timer()
        timer2.init(freq=(1/time_interval), mode=Timer.PERIODIC, callback=tick)