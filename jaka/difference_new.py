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
    # plt_keys = sorted(plt_keys, key=lambda x: int(re.findall(r'\d+', x)[0]))

    max_val = 0
    for key in plt_keys:
        key_max = np.max(abs(data[key] - data[key][0]))
        max_val = max_val if key_max < max_val else key_max

    #for i, key in enumerate(plt_keys):
    #    sim_sum[sim-1] += abs(np.average(data[key][:int(len(data)/2)-5]) - np.average(data[key][len(data)//2+5:]))/max_val


    for i, key in enumerate(plt_keys):
        tmp = ((np.average(data[key][:len(data[key]) // 2 - 5]) - np.average(data[key][len(data[key]) // 2 + 5:])) / max_val)
        sim_sum[sim-1] = sim_sum[sim-1] if abs(sim_sum[sim-1]) > abs(tmp) else tmp

    #for i, key in enumerate(plt_keys):
    #    sim_sum[sim - 1] += (np.average(data[key][:len(data) // 2 - 5]) - np.average(data[key][len(data) // 2 + 5:])) / max_val

plt.bar(range(1, len(sim_sum)+1), sim_sum)
plt.xticks(range(1,25))
# plt.title("sim" + str(sim))
# plt.legend()

plt.show()
