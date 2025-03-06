from .base_input import DigitalInput
from machine import Timer
from .interface import Tank

class LineSensor:
    
    """class containing the 4 line sesnors and relevant functions"""
    # define the sensors as pin inputs
    def __init__(self, tank, sensor_1_pin, sensor_2_pin, sensor_3_pin, sensor_4_pin):
        self.sensor1 = DigitalInput(sensor_1_pin)
        self.sensor2 = DigitalInput(sensor_2_pin)
        self.sensor3 = DigitalInput(sensor_3_pin)
        self.sensor4 = DigitalInput(sensor_4_pin)
        
        # tank must be a tank object. raise objection if not
        self.tank = tank
        if type(tank) != Tank:
            raise TypeError("tank parameter must be a tank object")
            
        self.integral = 0
        self.x_values = []
    
    def line_follow(self, time_interval, v_f):
        """uses the line sensors and drives the tank forward at speed v_f"""
        
        def control_function(self):
            # weighting for the sensors
            x = self.sensor1 * 2 + self.sensor2 - self.sesnor3 - self.sesnor4 * 2
            self.x_values.append(x)
            
            # PID controller
            kp = 0.1
            kd = 0
            ki = 0
            x_diff = x[-1] - x[-2]           
            result = kp * x + kd * x_diff + ki * self.integral
            return result
        
        def integrate(self, time_interval):
            self.integral += control_function(self) * time_interval
            self.tank.drive(v_f, control_function(self))
                 
        timer = Timer()
        timer.init(freq=(1/time_interval), mode=Timer.PERIODIC, callback=integrate)       