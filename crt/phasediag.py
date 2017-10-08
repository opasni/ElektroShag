import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re


simulations = range(1,24)

for sim in simulations:
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

    vzorec_u = "N.*_P1"
    vzorec_au = "N.*_f"
    reg_u = re.compile(vzorec_u)
    reg_au = re.compile(vzorec_au)

    plt_keys_u =  list(filter(reg_u.match, data.keys()))
    plt_keys_au = list(filter(reg_au.match, data.keys()))
    for kidx in range(len(plt_keys_u)-8):
        plt.plot(np.average(data[plt_keys_u[kidx]][-100:]), np.average(data[plt_keys_au[kidx]][-100:]), '.', label="sim"+str(sim) + " N" + str(kidx))

plt.legend()
plt.show()
