import matplotlib.pyplot as plt
import numpy as np
import serial
from time import sleep


board = serial.Serial("COM4", 115200, timeout=10)

speeds = 3
steps = 5


def times(n):
	out = list()
	for i in zip(range(n+1), board):
		if i[0]:
			out.append(int(i[1]))
	return np.array(out)

all_ts = times(speeds * steps)


with open("out.txt", "w") as f:
	f.write(np.array2string(all_ts, separator=", "))
print(np.array2string(all_ts, separator=", "))
