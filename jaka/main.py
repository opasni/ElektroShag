import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re

sim = 5
datafile = "../Data/Simul/Sim5.csv"
data = dict()
with open(datafile) as dat_f:
    reader = csv.DictReader(dat_f, delimiter=";")
    num_cols = sum(1 for r in reader)
    print("num", num_cols)
    dat_f.seek(0)
    reader = csv.DictReader(dat_f, delimiter=";")

    time_arr = []
    row_idx = 0
    for row in reader:
        print(row_idx)
        for key in row:
            if key not in data:
                data[key] = np.full(num_cols, np.nan)

            if key == "Time":
                time_arr.append(datetime.strptime(row[key], '%Y-%m-%d %H:%M:%S.%f'))
            else:
                data[key][row_idx] = row[key]

        row_idx += 1

# data = dict()
# time_arr = []
# for key in arr[0]:
#     data[key] = np.zeros(len(arr))

# for i,line in enumerate(arr):
#     for key in arr[0]:
#         if key == 'Time':
#             time_arr.append(datetime.strptime(line[key], '%Y-%m-%d %H:%M:%S.%f'))
#         else:
#             data[key][i] = float(line[key])


# plt.format_xdata = mdates.DateFormatter('%Y-%m-%d %h-%m-%s.%')

# plt_keys = ["N1_au", "N2_au", "N10_au", "N15_au"]


# regex_vzorec = ["N.*_u", "N.*_au", "N.*_r", "N.*_P.*", "N.*_Q.*"]
regex_vzorec = ["N.*_P"]
# regex_vzorec = ["N.*_u", "N.*_au", "N.*_i.*", "N.*_ai.*", "N.*_P.*", "N.*_Q.*", "N.*_f", "N.*_r"]
for i, vzorec in enumerate(regex_vzorec):
    reg = re.compile(vzorec)

    plt_keys = list(filter(reg.match, data.keys()))

    max_val = 0
    for key in plt_keys:
        max_val = max_val if np.max(abs(data[key]-data[key][10])) < max_val else np.max(abs(data[key]-data[key][10]))

    plt.figure(i)
    for key in plt_keys:
        #plt.plot_date(time_arr, (data[key]-data[key][10])/max_val, '-', label=key)
        plt.plot_date(time_arr, (data[key]), '-', label=key)
        # plt.plot_date(time_arr, data[key], '-', label=key)


plt.title("sim" + str(sim))
plt.legend()

plt.show()
