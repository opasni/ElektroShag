import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import re


def get_max_vals(data, vzorec, N=14):
    reg = re.compile(vzorec)

    plt_keys = list(filter(reg.match, data.keys()))

    d = sorted([[key, np.amax(np.fabs(data[key][10:]-np.average(data[key][10:50])))] for key in plt_keys],
           key=lambda v: -v[1])
    keys = [x[0] for x in d[:N]]

    vals = [x[1] for x in d[:N]] # np.ndarray([x[1] for x in d[:5]], dtype=np.float64)
    return keys,vals


arr = []

with open("../Data/Simul/Sim1.csv") as dat_f:
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


# plt.format_xdata = mdates.DateFormatter('%Y-%m-%d %h-%m-%s.%')

# plt_keys = ["N1_au", "N2_au", "N10_au", "N15_au"]

# regex_vzorec = ["N.*_u", "N.*_au", "N.*_r", "N.*_P.*", "N.*_Q.*"]
# regex_vzorec = ["N.*_u", "N.*_au", "N.*_i.*", "N.*_ai.*", "N.*_P.*", "N.*_Q.*", "N.*_f", "N.*_r"]

keys, data = get_max_vals(data, "N.*_u")
plt.bar(range(len(data)), data)
plt.xticks(range(len(data)), keys, rotation=40)


plt.show()
