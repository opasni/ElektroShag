"""ali je power plant ali power line"""

from rezanje import rezanje
import matplotlib.pyplot as plt
import re
import numpy as np

sim_sum = np.zeros(13)

pp = [1, 14, 15, 17]
pl = [2, 3, 16, 18, 19, 20, 21, 22, 23]

for si, sim in enumerate(sorted(pp + pl)):
    print(sim)

    data = rezanje(sim)

    vzorec = "N.*_i"
    reg = re.compile(vzorec)
    plt_keys = list(filter(reg.match, data.keys()))
    # plt_keys = sorted(plt_keys, key=lambda x: int(re.findall(r'\d+', x)[0]))

    data_sum = np.zeros(99)  # len(data["Time"]))

    for key in plt_keys:
        data_sum = np.add(data_sum, data[key])

    avgl = abs(np.average(data_sum[:len(data_sum) // 2 - 5]))
    avgr = abs(np.average(data_sum[len(data_sum) // 2 + 5:]))
    sim_sum[si] = abs(avgl - avgr) / max(avgl, avgr)

for i in range(1, 4):
    plt.bar(pp[i-1], sim_sum[i-1], color="r")
for i in range(4, 13):
    plt.bar(pl[i-4], sim_sum[i-1], color="k")
plt.xticks(range(1, 14), sorted(pp + pl))

plt.show()