from config import *

from utime import sleep


def telemetry_out(get_telem_str, supress=True):
    def wrapper(fn):
        if OUTPUT_MODE == 0:
            return fn
        elif OUTPUT_MODE == 1 and supress:
            return get_telem_str
        else:
            def inner(*args):
                print(get_telem_str(*args))
                fn(*args)
            return inner
    return wrapper

def telemetry_in(indentifier, alt_fn, signal=None, wait=True):
    def wrapper(fn):
        if INPUT_MODE == 0:
            return fn
        else:
            force_wait = INPUT_MODE == 1
            def inner(*args):
                if signal != None:
                    print(signal(*args))
                global sim_command_inputs
                if not indentifier in sim_command_inputs:
                    sim_command_inputs[indentifier] = [None, False, True]
                if sim_command_inputs[indentifier][2]:
                    if wait:
                        sim_command_inputs[indentifier][1] = False
                        while not sim_command_inputs[indentifier][1]:
                            sleep(0.05)
                    if sim_command_inputs[indentifier][0] == None:
                        if force_wait:
                            found = False
                            for _ in range(100):
                                if sim_command_inputs[indentifier][1]:
                                    return alt_fn(sim_command_inputs[indentifier][0])
                            raise RuntimeError
                    else:
                        return alt_fn(sim_command_inputs[indentifier][0])
                return fn(*args)
            return inner
    return wrapper
