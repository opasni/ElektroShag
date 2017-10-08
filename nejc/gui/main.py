import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re
from iskanje import iskanje


def is_short_circut(test_data, center_cut=5):
    vzorec_P = "N.*_P"
    reg_P = re.compile(vzorec_P)
    plt_keys_P = list(filter(reg_P.match, test_data.keys()))

    max_val = 0
    for key_P in plt_keys_P:
        key_max = np.max([abs(x - test_data[key_P][0]) for x in test_data[key_P]])
        max_val = max_val if key_max < max_val else key_max

    max_diff = 0
    for i, key_P in enumerate(plt_keys_P):
        center = len(test_data[key_P])//2
        tmp = abs(np.average(test_data[key_P][:center - center_cut]) - np.average(test_data[key_P][center + center_cut:])) / max_val
        max_diff = max_diff if max_diff > tmp else tmp
    
    return max_diff < 0.5


reg_r = re.compile("N.*_f")
reg_P = re.compile("N.*_P")

sim = 5
datafile = "../Data/Simul/Sim4.csv"
# datafile = "../Data/Real/RealMeasurement9.csv"
data = dict()

with open(datafile) as dat_f:
    reader = csv.DictReader(dat_f, delimiter=";")

    iskalnik = iskanje(deriv=False, tol=20)
    next(reader)
    next(reader)
    next(reader)
    for row in reader:
        data, flag = iskalnik.send_row(row)

        plt_keys_r = list(filter(reg_r.match, data.keys()))
        plt_keys_P = list(filter(reg_P.match, data.keys()))
        if flag:
            plt.figure(1)
            plt.title("freq deriv")
            for key in plt_keys_r:
                plt.plot_date(data["Time"], data[key], '-', label=key)

            plt.figure(2)
            plt.title("P")
            for key in plt_keys_P:
                plt.plot_date(data["Time"], data[key], '-', label=key)

            plt.title(datafile)
            plt.legend()
            plt.show()

            print("Short circut: ", is_short_circut(data))
