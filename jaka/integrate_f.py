from rezanje import rezanje
import matplotlib.pyplot as plt
import re
import numpy as np

sim_freq = []

for sim in range(1,5):
    print(sim)
    
    data = rezanje(sim)
    
    #vzorec = "N.*_u"
    #vzorec = "N.*_P"
    #vzorec = "N.*_au"
    sim_freq_tmp = []
    vzorec_all = ["N.*_P", "N.*_u", "N.*_au"]
    for vzorec in vzorec_all:
        reg = re.compile(vzorec)
        plt_keys = list(filter(reg.match, data.keys()))
        
        freq_val = np.zeros(len(plt_keys))
        
        max_val = 0
        for key in plt_keys:
            key_max = np.max(abs(data[key] - data[key][0]))
            max_val = max_val if key_max < max_val else key_max
        
        #plt.plot(data[plt_keys[1]])
        for i, key in enumerate(plt_keys):
            freq_val[i] = np.sum(abs(data[key][int(len(data[plt_keys[1]])/2)-3:int(len(data[plt_keys[1]])/2)+3] - data[key][0]))/max_val
        
        s = sorted(zip(plt_keys, freq_val), key=lambda x:-x[1])
        # sim_freq_tmp.append(plt_keys[np.argmax(abs(freq_val)])
        sim_freq_tmp.append(s[:2])
    sim_freq.append(sim_freq_tmp)
print(sim_freq)
#plt.bar(range(1, len(sim_sum)+1), sim_sum)
#plt.xticks(range(1,len(plt_keys)+1),plt_keys,rotation="vertical")
# plt.title("sim" + str(sim))
#plt.legend()
#plt.plot(range(1,len(plt_keys)+1),freq_val)
#plt.show()