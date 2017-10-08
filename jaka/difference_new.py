""""
Prikaz ustrezne klasifikacije 3 pole short circut problema
"""

from rezanje import rezanje
import matplotlib.pyplot as plt
import re
import numpy as np

sim_sum = np.zeros(23)

for sim in range(1,24):
    print(sim)

    data = rezanje(sim)

    vzorec = "N.*_P"
    reg = re.compile(vzorec)
    plt_keys = list(filter(reg.match, data.keys()))

    max_val = 0
    for key in plt_keys:
        key_max = np.max(abs(data[key] - data[key][0]))
        max_val = max_val if key_max < max_val else key_max

    for i, key in enumerate(plt_keys):
        tmp = abs((np.average(data[key][:len(data[key]) // 2 - 5]) - np.average(data[key][len(data[key]) // 2 + 5:])) / max_val)
        sim_sum[sim-1] = sim_sum[sim-1] if abs(sim_sum[sim-1]) > abs(tmp) else tmp


plt.bar(range(1, 4), sim_sum[:3], color="k")
plt.bar(range(14, len(sim_sum)+1), sim_sum[13:], color="k", label="power plant + power line")

plt.bar(range(4, 14), sim_sum[3:13], color="r", label="3 pole short circut")

plt.xticks(range(1,25))
plt.legend()
plt.show()
