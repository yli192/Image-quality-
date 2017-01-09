#! /usr/bin/python
import sys
import numpy as np
import matplotlib.pylab as plt
import itertools
from scipy.optimize import curve_fit
import operator
# Gary Y. Li
# Jan 2017
def read_auc(txt,dict):
    for line in txt:
        line = line.strip().split(' ')
        dict[line[-1]]=[line[0]]

    return dict

def read_didx(txt,dict):
    for line in txt:
        line = line.strip().split(' ')
        for item in dict:
            if item == line[0]:
                #print dict[item]
                #dict.setdefault(item, [])
                dict[item].append(line[1])
    return dict

def func(x, a, b, c):
    y = a * np.exp(-b * x) + c
    return y

def main (args):
    if (len(args) != 2):
        print "Arguments: all_test_stats addnoise.log"
        exit();
    ts_file = open(args[0])
    noise_logfile = open(args[1])
    dict1={}
    dict1 = read_auc(ts_file,dict1)
    dict1 = read_didx(noise_logfile,dict1)
    #print dict1
    colors = "gry"
    color_index=0
    marker = itertools.cycle(('o', 'v', '^', '<', '>', 's', '8', 'p'))
    #change 10,50,90 to 50 below to plot fitted curve
    for hp in [10 ,50, 90]:
        didx=[]
        auc=[]
        for item in dict1:
            if (item.split('.')[1] == 'hp'+str(hp)):
                auc.append(float(dict1[item][0]))
                didx.append(float(dict1[item][1]))
        name = "hp" + str(hp)
        #activate below to plot fitted curve
        L= sorted(zip(didx,auc),key=operator.itemgetter(0))
        didx, auc = zip(*L)
        aucn = auc + 0.0001*np.random.normal(size=len(didx))
        popt, pcov = curve_fit(func, didx, aucn)
        plt.scatter(didx,auc,c=colors[color_index],marker=marker.next(),label=name)
        didx=np.asarray(didx)

        #activate below to plot fitted curve
        plt.plot(didx, func(didx, *popt), 'r-', label=' \n $y = %0.2f e^{%0.2f x} + %0.2f$' % (popt[0],-popt[1], popt[2]))
        plt.xlabel('detectability_idx')
        plt.ylabel('AUC value')
        plt.ylim([0.5,1])
        plt.xlim([0,15])
        plt.title('AUC vs. detectability_idx as alpha changes from 0.5 to 5, age 15')
        #plt.legend(['measured data',equation])
        color_index += 1


    #plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=12, bbox_to_anchor=(0.6, 0.8))
    plt.legend(bbox_to_anchor=(1, 0.8), fancybox=True, shadow=True)
    plt.show()
    #outfile = args[2]


main(sys.argv[1:])
