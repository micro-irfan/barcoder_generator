import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, date
from multiprocessing import Pool
import matplotlib.pyplot as plt
import sys
import math
import functools

def get_date_time():
    today = date.today()
    t = datetime.time(datetime.now())
    Time = str(t).split('.')[0]
    return str(today) + ' ' +  str(Time)

def hamdist(bc, HD, prefix, l):
    h_dict = dict.fromkeys(range(0, l+1), 0)
    File = open(prefix + 'poor_HD.txt', 'a+')

    for i in range(len(bc) - 1):
        for j in range(i + 1, len(bc), 1):
            h = 0
            h = sum(ch1 != ch2 for ch1, ch2 in zip(bc[i], bc[j]))
            if h < HD:
                File.write(bc[i] + '\t' + bc[j] + '\t' + str(h) + '\n')
            h_dict[h] += 1

    File.close()
    return h_dict

def create_histo(dictionary, prefix):
    plt.figure(figsize=(12, 6), dpi=128)
    plt.switch_backend('agg')
    plt.bar(list(dictionary.keys()), dictionary.values(), color='g')
    plt.savefig(prefix + 'histogram_plot.png')

def is_float_try(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
        
def main_process(lib, n_sample, p, prefix, m, HD, l):
    print ("Processing Begins at: " + get_date_time())
 
    f = functools.partial(hamdist, l=l)
    f1 = functools.partial(f, HD=HD)
    f2 = functools.partial(f1, prefix=prefix)

    hd_sample20 = p.map(f2, [[lib[x] for x in random.sample(
        range(len(lib)), n_sample)] for _ in range(m)])
    total_dict = dict.fromkeys(range(0, 21), 0)

    summary = open(prefix + 'summary.txt', 'a+')
    for h, i in enumerate(hd_sample20):
        for key, value in i.items():
            total_dict[key] += value
            summary.write('Sample ' + str(h) + '\t' +
                          str(key) + ': ' + str(value) + '\n')
            if key == l:
                summary.write('\n')

    for key, value in total_dict.items():
        summary.write('Sampling Summary' + '\t' +
                      str(key) + ': ' + str(value / 20) + '\n')

    summary.close()
    total_dict = dict((k, v / len(hd_sample20)) for k, v in total_dict.items())
    create_histo(total_dict, prefix)

    print ("Processing Ended at: " + get_date_time())

if __name__ == '__main__':
    arguments = sys.argv[1:]
    n = int(arguments[0])
    l = int(arguments[1])
    assert l < 50
    R = int(arguments[2])
    m = int(arguments[3])
    HD = float(arguments[4])

    if HD < 1:
        HD = math.ceil(HD * l)

    t = arguments[5]

    # Argument for CPU and Prefix is optional
    if is_float_try(t):
        if arguments[6]:
            prefix = arguments[6] + '_'
        else:
            prefix = ''
        t = int(arguments[5])
    else:
        t = 1
        if arguments[5]:
            prefix = arguments[5] + '_'
        else:
            prefix = ''

    lib = [(''.join(random.choice('ACGT') for _ in range(l)))
           for _ in range(n)]

    File = open(prefix + 'random_sequences_generated.txt', 'w')
    File.writelines([x + '\n' for x in lib])
    File.close()

    n_sample = R
    p = Pool(t)
    main_process(lib, n_sample, p, prefix, m, HD, l)
