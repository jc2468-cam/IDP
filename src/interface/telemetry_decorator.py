from config import *

from utime import sleep


def telemetry_out(get_telem_str, suppress=True):
    """Outputs a telemetry message over serial to a host computer instead of / as well as performing a function, depending in the config file.

    Arguments:
        `get_telem_str` (`function`): A function to call (with the arguments passed to the output function) to generate the telemetry message.
        `suppress` (`bool`): Whether to skip calling this function when 'telemetry only' mode is set in the config file (default `True`).
    """
    def wrapper(fn):
        if OUTPUT_MODE == 0:
            return fn
        elif OUTPUT_MODE == 1 and suppress:
            return lambda *args: print(get_telem_str(*args))
        else:
            def inner(*args):
                print(get_telem_str(*args))
                fn(*args)
            return inner
    return wrapper

def telemetry_in(indentifier, alt_fn, signal=None, wait=True):
    """Allows the output of a function to be controlled from a host computer over serial, depending on the config file.

    Arguments:
        `identifier` (`str`): The identifier the host computer will use to refer to this function.
        `alt_fn` (`function`): The function used to parse commands from the host computer and generate a simulated output.
        `signal` (`function`): Generate a telemetry string to be output over serial when this function is called (optional).
        `wait` (`float`): Wait a timeout (given in seconds) before giving a simulated output (to allow the host to respond with an instruction) (optional).
    """
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
