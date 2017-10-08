#import csv
import pandas as pd
from rezanje import rezanje
import matplotlib.pyplot as plt
import re
import numpy as np

#sim_freq = []

def get_number(s, vzorec):
    if vzorec=="N.*_P":
        return  list(map(int,re.findall(r'\d+', s)))
    else:
        return int(re.findall(r'\d+', s)[0])

def get_best_bets(sim):    
    data = rezanje(sim)
    sim_freq_tmp = []
    #vzorec_all = ["N.*_P", "N.*_u", "N.*_au", "N.*_i"]
    #vzorec_all = ["N.*_P", "N.*_au", "N.*_i"]
    vzorec_all = ["N.*_au"]
    
    for vzorec in vzorec_all:
        reg = re.compile(vzorec)
        plt_keys = list(filter(reg.match, data.keys()))
        
        freq_val = np.zeros(len(plt_keys))
        
        max_val = 0
        for key in plt_keys:
            key_max = np.max(abs(data[key] - data[key][0]))
            max_val = max_val if key_max < max_val else key_max
        
        for i, key in enumerate(plt_keys):
            freq_val[i] = np.sum(abs(data[key][int(len(data[plt_keys[1]])/2)-3:int(len(data[plt_keys[1]])/2)+3] - data[key][0]))/max_val
        
        s = sorted(zip(plt_keys, freq_val), key=lambda x:-x[1])
        # sim_freq_tmp.append(plt_keys[np.argmax(abs(freq_val)])
        sim_freq_tmp.append([(x[0],get_number(x[0], vzorec),x[1]) for x in s])
    #sim_freq.append(sim_freq_tmp)
    return(sim_freq_tmp)
    
def predict_nodes(predicts):
    nodes_predict = []
    for source in predicts:
        #print (source)
        if 'a' in source[0]:
            nodes_predict.append(source[1:])
        #elif 'P' in source[0]:
        #    return 0
        #else:
        #    return source[0]
    return nodes_predict

final_data = []

for sim in range(1,24):
    print (sim)
    predict = get_best_bets(sim)
    for pre_sor in predict:
        #print(predict_nodes(pre_sor))
        final_data.append(predict_nodes(pre_sor))
    #print (final_data)

my_out_data = pd.DataFrame(final_data)

my_out_data.to_csv('pointsrelations.csv', index=False, header=False)
#print(sim_freq)