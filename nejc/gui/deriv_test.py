import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re
from derivative import deriv3



arr = []

sim = 7

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



vzorec_f = "N.*_f"
vzorec_r = "N.*_r"
r_f = re.compile(vzorec_f)
r_r = re.compile(vzorec_r)

plt_keys_f = sorted(list(filter(r_f.match, data.keys())))
plt_keys_r = sorted(list(filter(r_r.match, data.keys())))

key_f = plt_keys_f[0]
key_r = plt_keys_r[0]
print(key_f, key_r)
plt.plot_date(time_arr, data[key_r], '-', label="_r")

new_data = np.zeros(len(data[key_r]))
for i in range(1,len(data[key_r])-1):
    new_data[i] = deriv3(data[key_f][i-1],data[key_f][i+1])

plt.plot_date(time_arr, new_data, '-', label="deriv3")

plt.figure(2)
plt.semilogy(time_arr, abs(new_data-data[key_r]), '-', label="deriv3")

plt.title("sim" + str(sim))
plt.legend()

plt.show()