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

    # TODO to je jeba!!!
    data_sum = np.zeros(99)  # len(data["Time"]))

    for key in plt_keys:
        data_sum = np.add(data_sum, data[key])

    avgl = abs(np.average(data_sum[:len(data_sum) // 2 - 5]))
    avgr = abs(np.average(data_sum[len(data_sum) // 2 + 5:]))
    sim_sum[si] = abs(avgl - avgr) / max(avgl, avgr)

plt.bar(range(1, 14), sim_sum)
plt.xticks(range(1, 14), sorted(pp + pl))
# plt.title("sim" + str(sim))
# plt.legend()

plt.show()