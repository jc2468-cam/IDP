from interface.col_sense import *
from machine import Pin


class DigitalInput:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
    def value(self):
        return self.pin.value()
    def bind_interupt(self, callback, edge_id):
        edge = [Pin.IRQ_FALLING, Pin.IRQ_RISING][edge_id]
        self.pin.irq(callback, edge)
    def bind_interupt_falling(self, callback):
        self.bind_interupt(callback, 0)
    def bind_interupt_rising(self, callback):
        self.bind_interupt(callback, 1)
