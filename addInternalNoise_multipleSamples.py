#! /usr/bin/python
import sys
import numpy as np
# Gary Y. Li
# Dec 2016
def readTestStats(ts_file):
    line_num = 0
    ts_class1 = []
    ts_class2 = []
    for line in ts_file:
        line = line.strip()
        if (line == "large"):
            line_num += 1
        elif (line == "*"):
            line_num += 1
        if (line_num == 1 ):
            ts_class1.append(line)
        if (line_num == 2 ):
            ts_class2.append(line)

    return ts_class1[1:], ts_class2[1:]

def writeTestStats(ts_class1,ts_class2,outfile):
    r = open(outfile,'a')
    r.write("firstline\nlarge\n")
    for i in range(len(ts_class1)):
         r.write("%s\n" % (ts_class1[i]))
    r.write("*\n")
    for i in range(len(ts_class2)):
        r.write("%s\n" % (ts_class2[i]))
    r.write("*\n")
    r.close

def main (args):
    if (len(args) != 3):
        print "Arguments: test_stats file alpha outfile"
        exit();
    ts_file = open(args[0])
    alpha = float(args[1])
    outfile = args[2]
    [ts_class1,ts_class2] = readTestStats(ts_file)
    ts_class1=np.asarray(ts_class1); ts_class1 = ts_class1.astype(np.float)
    ts_class2=np.asarray(ts_class2); ts_class2 = ts_class2.astype(np.float)
    #print np.mean(ts_class1),np.mean(ts_class2), np.std(ts_class1), np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    num_samples=200
    print "alpha=",alpha, ",samples drawn=",num_samples
    noisy_ts_all=[]
    for i in range(num_samples):
        np.random.seed(seed=i)
        noisy_ts = np.random.normal(np.mean(ts_class1), np.std(ts_class1), len(ts_class1))
        noisy_ts_all.append(noisy_ts)
        #print "std, max and min of added_ts,std, max and min of alpha*added_ts",np.std(noisy_ts),np.max(noisy_ts),np.min(noisy_ts),np.std(noisy_ts*alpha),np.max(noisy_ts*alpha),np.min(noisy_ts*alpha)
    noisy_ts_mean=np.average(noisy_ts_all,axis=0)
    print "mean and std of noisy_ts_mean",np.mean(noisy_ts_mean),np.std(noisy_ts_mean),np.mean(noisy_ts),np.std(noisy_ts)
    print "mean and std of ts_class1,2 before adding noise",np.mean(ts_class1), np.std(ts_class1), np.mean(ts_class2),np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    ts_class1 = ts_class1 + alpha*noisy_ts_mean
    #print np.sum(np.multiply(alpha,noisy_ts))
    ts_class2 = ts_class2 + alpha*noisy_ts_mean
    print "mean and std of ts_class1,2 after adding noise",np.mean(ts_class1), np.std(ts_class1), np.mean(ts_class2),np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    #writeTestStats(ts_class1,ts_class2,outfile)

main(sys.argv[1:])
