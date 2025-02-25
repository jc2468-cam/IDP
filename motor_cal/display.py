import matplotlib.pyplot as plt
import numpy as np


file_name = "out_0_3.txt"

with open(file_name, "r") as f:
	ts = np.array([int(i) for i in f.read().strip()[1:-1].split(",")])


fig, ax1 = plt.subplots()

i0, steps = 0, ts.shape[0]
ts = ts[i0: i0 + steps] - ts[i0]

dts = ts[1:] - ts[:-1]
mean_t = ts[-1] / ((steps - 1) * 1000)
std_t = np.std(dts)
print("average freq:", 1 / mean_t)
print("standard deviation:", std_t)
ax1.scatter(np.linspace(0,1,ts.shape[0]), ts)

plt.show()
