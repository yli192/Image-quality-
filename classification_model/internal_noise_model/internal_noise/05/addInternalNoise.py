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
        print "Arguments: test_stats_file alpha outfile"
        exit();
    ts_file = open(args[0])
    alpha = float(args[1])
    outfile = args[2]
    [ts_class1,ts_class2] = readTestStats(ts_file)
    ts_class1=np.asarray(ts_class1); ts_class1 = ts_class1.astype(np.float)
    ts_class2=np.asarray(ts_class2); ts_class2 = ts_class2.astype(np.float)
    #print "alpha=",alpha,args[0]
    #print "mean and std of ts_class1,2 before adding noise", np.mean(ts_class1),np.mean(ts_class2), np.std(ts_class1), np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    noisy_ts = np.random.normal(np.mean(ts_class1), np.std(ts_class1), len(ts_class1))
    ts_class1 = ts_class1 + alpha*noisy_ts
    #print np.sum(np.multiply(alpha,noisy_ts))
    ts_class2 = ts_class2 + alpha*noisy_ts
    #print "mean and std of ts_class1,2 after adding noise", np.mean(ts_class1),np.mean(ts_class2), np.std(ts_class1), np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    d_idx = (np.mean(ts_class1)-np.mean(ts_class2))**2/(0.5*(np.std(ts_class1)**2+np.std(ts_class2)**2))
    ts_id = args[0].strip().split(".")[0:4]
    if float(args[1]).is_integer():
        ts_id.append('alpha'+str(int(args[1])))
    else:
        ts_id.append('alpha'+str(float(args[1])))
    ts_id.append('ts')
    ts_id = '.'.join(ts_id)
    print ts_id,d_idx, alpha
    #writeTestStats(ts_class1,ts_class2,outfile)

main(sys.argv[1:])
