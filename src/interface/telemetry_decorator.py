from utime import sleep


def telemetry_out(get_telem_str):
	def wrapper(fn):
		def inner(*args):
			global INPUT_MODE
			if INPUT_MODE == 1 || INPUT_MODE == 2:
				print(get_telem_str(*args))
			if INPUT_MODE == 0 || INPUT_MODE == 2:
				fn(*args)
		return inner
	return wrapper

def telemetry_in(indentifier, alt_fn, signal=None, wait=True):
	def wrapper(fn):
		def inner(*args):
			global INPUT_MODE
			if INPUT_MODE == 1 or INPUT_MODE == 2:
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
						if INPUT_MODE == 1:
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
