import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re

sim_sum = np.zeros(23)

for sim in range(1,24):
    print(sim)

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
    # plt_keys = sorted(plt_keys, key=lambda x: int(re.findall(r'\d+', x)[0]))

    max_val = 0
    for key in plt_keys:
        key_max = np.max(abs(data[key][10:] - data[key][10]))
        max_val = max_val if key_max < max_val else key_max

    for i, key in enumerate(plt_keys):
        sim_sum[sim-1] += abs(np.average(data[key][10:510]) - np.average(data[key][-500:]))/max_val

    #for i, key in enumerate(plt_keys):
    #    tmp = abs((np.average(data[key][10:510]) - np.average(data[key][-500:])) / max_val)
    #    sim_sum[sim-1] = sim_sum[sim-1] if abs(sim_sum[sim-1]) > tmp else tmp

b = sorted(zip(range(1,24), sim_sum), key=lambda x: -abs(x[1]))
lab = [x[0] for x in b]
vls = [x[1] for x in b]

# plt.bar(range(1, len(sim_sum)+1), vls)
# plt.xticks(range(1,25), lab)

plt.bar(range(1, len(sim_sum)+1), sim_sum)
plt.xticks(range(1,25))
# plt.title("sim" + str(sim))
plt.legend()

plt.show()
