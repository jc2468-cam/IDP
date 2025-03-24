ON_PICO = True

from config import INPUT_MODE
from interface.col_sense import *

from utime import sleep
from machine import Pin


class DigitalInput:
    """Represents a digital input pin, and allows simulated control from a host computer (based on a config file)."""
    def __init__(self, pin_id):
        """Create a new `DigitalInput`

        Arguments:
            `pin_id` (`int`): The GPIO pin number to get input from.

        Returns:
            `DigitalInput`: The wrapped input pin.
        """
        self.pin_id = pin_id
        self.pin = Pin(pin_id, Pin.IN, Pin.PULL_DOWN)
    def value(self):
        """Read the value of the input pin / the last simulated input.

        Returns:
            `int`: The last set value of the pin.
        """
        global INPUT_MODE
        if INPUT_MODE == 0:
            return self.pin.value()
        elif INPUT_MODE == 1:
            global sim_input_pins
            return sim_input_pins[self.pin_id][0]
        elif INPUT_MODE == 2:
            global sim_input_pins
            next_val = self.pin.value()
            if next_val == sim_input_pins[self.pin_id][1]:
                return latest_pin_value(self.pin_id)
            else:
                sim_input_pins[self.pin_id][1] = next_val
                sim_input_pins[self.pin_id][2] = True
                return next_val
        else:
            raise RuntimeError
    def bind_interrupt(self, callback, edge_id):
        """Bind an interrupt callback to the rising or falling edge of the input pin / simulated input.

        Arguments:
            `callback` (`function`): The callback to run when the interrupt is triggered.
            `edge_id` (`int`): The edge to trigger the interrupt on (`0` for falling, `1` for rising - to allow setting from a returned pin value).
        """
        global INPUT_MODE
        if INPUT_MODE == 0 or INPUT_MODE == 2:
            edge = [Pin.IRQ_FALLING, Pin.IRQ_RISING][edge_id]
            self.pin.irq(callback, edge)
        if INPUT_MODE == 1 or INPUT_MODE == 2:
            global sim_pin_interrupt_callbacks
            sim_pin_interrupt_callbacks[self.pin_id] = (callback, edge_id)
    def bind_interrupt_falling(self, callback):
        """Bind an interrupt callback to the falling edge of an input - see `bind_interrupt`."""
        self.bind_interrupt(callback, 0)
    def bind_interrupt_rising(self, callback):
        """Bind an interrupt callback to the rising edge of an input - see `bind_interrupt`."""
        self.bind_interrupt(callback, 1)


def null_callback(p):
    """An empty function to bind as a default callback when setting up simulated inputs"""
    pass

def start_input_sim_monitor():
    """Starts monitoring for simulation instructions from a host computer over the serial link.

    This process runs in a separate thread so that it does not interfere with the main control flow.
    """
    def inner():
        global sim_input_pins, sim_pin_interrupt_callbacks, sim_command_inputs
        # [simulated, real, last updated index]
        sim_input_pins = [[0, 0, 1] for _ in range(28)]
        sim_pin_interrupt_callbacks = [(null_callback, 0) for _ in range(28)]
        sim_command_inputs = dict()

        while True:
            command = input().strip()
            if command == "~":
                sleep(0.3)
            elif command[:9] == "Control::":
                if command[9:16] == "set_pin":
                    print(command[17:-1].split(","))
                    p, v = [int(s) for s in command[17:-1].split(",")]
                    old_v = sim_input_pins[p][sim_input_pins[p][2]]
                    sim_input_pins[p][0] = v
                    sim_input_pins[p][1] = 0
                    if old_v != v and sim_pin_interrupt_callbacks[p][1] == v:
                        sim_pin_interrupt_callbacks[p][0](p)
                elif "#" in command[9:]:
                    identifier = command[9:].split("#")
                elif command[9:13] == "kill":
                    print("Stopping input thread")
                    break
                else:
                    identifier = command[9:].split("(")[0]
                    sim_command_inputs[identifier] = [command[9:], 1]

    if ON_PICO:
        import _thread
        _thread.start_new_thread(inner, ())

def latest_pin_value(pin_id):
    """Returns the most recently set value for a pin enabled in the config file (either the physical voltage or simulated input)."""
    global sim_input_pins
    return sim_input_pins[pin_id][sim_input_pins[pin_id][2]]
