import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re


sim = 14

arr = []
with open("../Data/Simul/Sim" + str(sim) + ".csv") as dat_f:
    reader = csv.DictReader(dat_f, delimiter=";")
    for row in reader:
        arr.append(row)

data = dict()
time_arr = []
for key in arr[0]:
     data[key] = np.zeros(len(arr))

for i,line in enumerate(arr):
    for key in arr[0]:
        if key == 'Time':
            time_arr.append(datetime.strptime(line[key], '%Y-%m-%d %H:%M:%S.%f'))
        else:
            data[key][i] = float(line[key])


vzorec = "N.*_P"
reg = re.compile(vzorec)
plt_keys = list(filter(reg.match, data.keys()))
plt_keys = sorted(plt_keys, key=lambda x: int(re.findall(r'\d+', x)[0]))

max_val = 0
for key in plt_keys:
    key_max = np.max(abs(data[key][10:] - data[key][10]))
    max_val = max_val if key_max < max_val else key_max

vals = np.zeros(len(plt_keys))

for i, key in enumerate(plt_keys):
    vals[i] = (np.average(data[key][10:510]) - np.average(data[key][-500:]))/max_val

plt.bar(range(len(vals)), vals)
plt.xticks(range(len(vals)), plt_keys, rotation="vertical")
print(plt_keys)
plt.title("sim" + str(sim))
plt.legend()

plt.show()
