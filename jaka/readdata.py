import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import re


arr = []

with open("../Data/Simul/Sim12.csv") as dat_f:
    reader = csv.DictReader(dat_f, delimiter=";")
    for row in reader:
        arr.append(row)


data = dict()
for key in arr[0]:
     data[key] = []

for line in arr:
    for key in arr[0]:
        if key == 'Time':
            data[key].append(datetime.strptime(line[key], '%Y-%m-%d %H:%M:%S.%f'))
        else:
            data[key].append(float(line[key]))


# plt.format_xdata = mdates.DateFormatter('%Y-%m-%d %h-%m-%s.%')

# plt_keys = ["N1_au", "N2_au", "N10_au", "N15_au"]

reg = re.compile("N.*_au")
plt_keys = list(filter(r.match, data.keys()))

for key in plt_keys:
    plt.plot_date(data['Time'], data[key]/np.amax(data[key]), '-', label=key)

plt.legend()
plt.show()
