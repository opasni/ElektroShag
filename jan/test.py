from iskanje import iskanje
import numpy as np
import re
import matplotlib.pyplot as plt

def plot(data):
    time_arr = []
    for i in range(len(data['Time'])):
        time_arr.append(i * 0.02)

    regex_vzorec = ["N.*_r"]
    # regex_vzorec = ["N.*_u", "N.*_au", "N.*_i.*", "N.*_ai.*", "N.*_P.*", "N.*_Q.*", "N.*_f", "N.*_r"]
    for i, vzorec in enumerate(regex_vzorec):
        reg = re.compile(vzorec)

        plt_keys = list(filter(reg.match, data.keys()))
        plt.figure(i)
        for key in plt_keys:
            plt.plot_date(data['Time'], (data[key]), '-', label=key)
        plt.legend()
    plt.show()


mygen = iskanje(1)
for j in range(100000):
    a = next(mygen)
    if a != 0:
        plot(a)
