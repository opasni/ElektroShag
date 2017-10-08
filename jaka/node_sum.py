import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re

pp = [1, 14, 15, 17]
pl = [2, 3, 16, 18, 19, 20, 21, 22, 23]

for si, sim in enumerate(pp): # enumerate(list(range(1,4)) + list(range(14,17))):

    arr = []
    print(sim)

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


    vzorec = "N.*_i"
    reg = re.compile(vzorec)

    plt_keys = list(filter(reg.match, data.keys()))

    node_dict = dict()

    for key in plt_keys:
        N_idx = int(re.findall(r'\d+', key)[0])
        if N_idx in node_dict:
            node_dict[N_idx] = np.add(node_dict[N_idx], data[key])
        else:
            node_dict[N_idx] = np.zeros(len(data["Time"]))
            node_dict[N_idx] = np.add(node_dict[N_idx], data[key])

    print(plt_keys)

    plt.figure(si)
    for idx in node_dict:
        plt.plot_date(time_arr, node_dict[idx], '-', label=idx)

    full_sum = np.zeros(len(data["Time"]))
    for idx in node_dict:
        full_sum = np.add(full_sum, node_dict[idx])

    plt.plot_date(time_arr, full_sum, '-', linewidth=3, label="full")



    plt.title("sim" + str(sim))
    plt.legend()

plt.show()