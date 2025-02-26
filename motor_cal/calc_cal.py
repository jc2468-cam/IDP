import os


cal_p, cal_s = list(), list()

file_names = [f for f in os.listdir() if f.split(".")[-1] == "txt"]
print(file_names)

for f_name in file_names:
	x = float(f_name.split(".")[0][4:].replace("_", "."))
	with open(f_name, "r") as f:
		ts = [int(i) for i in f.read().strip()[1:-1].split(",")]
	mean_t = (ts[-1] - ts[0]) / ((len(ts) - 1) * 1000)
	cal_p.append(x)
	cal_s.append(1/mean_t)

print(cal_p)
print(cal_s)
