import matplotlib.pyplot as plt
import numpy as np
import os


cal_p, cal_s = list(), list()

file_names = [f for f in os.listdir() if f.split(".")[-1] == "txt"]
print(file_names)

for f_name in file_names:
	x = float(f_name.split(".")[0][4:].replace("_", "."))
	if x > 1.0:
		break
	with open(f_name, "r") as f:
		ts = [int(i) for i in f.read().strip()[1:-1].split(",")]
	mean_t = (ts[-1] - ts[0]) / ((len(ts) - 1) * 1000)
	cal_p.append(x)
	cal_s.append(1/mean_t)

cal_p, cal_s = np.array(cal_p), np.array(cal_s)
m, c = np.polyfit(cal_p, cal_s, 1)
print(cal_p)
print(cal_s)
print(f"linear fit: s = {m} * p + {c}")

fig, ax = plt.subplots()

ax.plot(cal_p, cal_s)

plt.show()
