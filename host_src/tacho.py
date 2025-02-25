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

fig, ax1 = plt.subplots()

for i0 in range(0, speeds * steps, steps):
	ts = all_ts[i0: i0 + steps]
	dts = ts[1:] - ts[:-1]
	mean_t = ts[-1] / ((steps - 1) * 1000)
	var_t = np.var(dt)
	print("average freq:", 1 / mean_t)
	print("variance:", var_t)
	ax1.scatter(np.linspace(0,1,ts.shape[0]), ts)

plt.show()
