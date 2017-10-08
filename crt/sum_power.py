import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import re


for sim in range(1,6):

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


    vzorec = "N.*_P.*"
    reg = re.compile(vzorec)

    plt_keys = list(filter(reg.match, data.keys()))
    print(plt_keys)
    power_sum = np.zeros(len(time_arr))
    for i in range(len(time_arr)):
        power_sum[i] = sum([data[key][i] for key in plt_keys])

    plt.plot_date(time_arr[10:], power_sum[10:] - np.average(power_sum[10:50]), '-', label=str(sim))

plt.legend()
plt.show()