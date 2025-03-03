ON_PICO = True


class DigitalInput:
    def __init__(self, pin):
        self.pin = pin
    def value(self):
        global sim_input_pins
        return sim_input_pins[self.pin]
    def bind_interupt(self, callback, edge_id):
        global sim_pin_interupt_callbacks
        sim_pin_interupt_callbacks[self.pin] = (callback, edge_id)
    def bind_interupt_falling(self, callback):
        self.bind_interupt(callback, 0)
    def bind_interupt_rising(self, callback):
        self.bind_interupt(callback, 1)


def null_callback(p):
    pass

def start_input_sim_monitor():
    def inner():
        global sim_input_pins, sim_pin_interupt_callbacks
        sim_input_pins = [0 for _ in range(28)]
        sim_pin_interupt_callbacks = [(null_callback, 0) for _ in range(28)]

        while True:
            command = input().strip()
            if command[:16] == "Control::set_pin":
                p, v = *[int(s) for s in command[1:-1].split(",")]
                old_v = sim_input_pins[p]
                sim_input_pins[p] = v
                if old_v != v && sim_pin_interupt_callbacks[p][1] == v:
                    sim_pin_interupt_callbacks[p][0](p)

    if ON_PICO:
        import _thread
        _thread.start_new_thread(inner, ())
