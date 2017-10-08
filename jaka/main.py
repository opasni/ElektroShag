import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re


def is_short_circut(test_data, center_cut=5):
    vzorec_P = "N.*_P"
    reg_P = re.compile(vzorec_P)
    plt_keys_P = list(filter(reg_P.match, test_data.keys()))

    max_val = 0
    for key_P in plt_keys_P:
        key_max = np.max(abs(test_data[key_P] - test_data[key_P][0]))
        max_val = max_val if key_max < max_val else key_max

    max_diff = 0
    for i, key_P in enumerate(plt_keys_P):
        center = len(test_data[key_P])//2
        tmp = abs(np.average(test_data[key_P][:center - center_cut]) - np.average(test_data[key_P][center + center_cut:])) / max_val
        max_diff = max_diff if max_diff > tmp else tmp
    
    return max_diff < 0.5


vzorec = "N.*_P"
reg = re.compile(vzorec)

sim = 5
datafile = "../Data/Simul/Sim5.csv"
data = dict()
with open(datafile) as dat_f:
    reader = csv.DictReader(dat_f, delimiter=";")

    #iskalnik = janova_koda()
    for row in reader:
        iskalnik.send_row(row)
        data = next(iskalnik)

        plt_keys = list(filter(reg.match, data.keys()))
        if data != 0:
            for key in plt_keys:
                plt.plot_date(data["Time"], (data[key]), '-', label=key)

            plt.title(datafile)
            plt.legend()
            plt.show()

            print("Short circut: ", is_short_circut(data))

            