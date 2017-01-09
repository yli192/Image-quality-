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
def calc_alpha(target_detectability_idx,ts_class1,ts_class2,noisy_ts):
    mu_1= np.mean(ts_class1)
    mu_2= np.mean(ts_class2)
    std_1 = np.std(ts_class1)
    std_2 = np.std(ts_class2)
    inital_d_idx = (mu_1-mu_2)**2/(0.5*(std_1**2+std_2**2))

    alpha = 0.5
    while (abs(target_detectability_idx-inital_d_idx) > 0.05):
        if target_detectability_idx > inital_d_idx:
        #increase alpha
            alpha = alpha - 0.01
        elif target_detectability_idx < inital_d_idx:
        #decrease alpha
            alpha = alpha + 0.01
    #gen new ts with alpha
        ts_class1_new = ts_class1 + alpha*noisy_ts
        ts_class2_new = ts_class2 + alpha*noisy_ts
        mu_1_new= np.mean(ts_class1_new)
        mu_2_new= np.mean(ts_class2_new)
        std_1_new = np.std(ts_class1_new)
        std_2_new = np.std(ts_class2_new)
        d_idx = (mu_1_new-mu_2_new)**2/(0.5*(std_1_new**2+std_2_new**2))
        #if d_idx
        inital_d_idx = d_idx

    return alpha
def main (args):
    if (len(args) != 4):
        print "Arguments: test_stats_file detectability_idx sample_multiplier outfile"
        exit();
    ts_file = open(args[0])
    target_d_idx = float(args[1])
    sample_multiplier=int(args[2])
    outfile = args[3]
    [ts_class1,ts_class2] = readTestStats(ts_file)
    ts_class1=np.asarray(ts_class1); ts_class1 = ts_class1.astype(np.float)
    ts_class2=np.asarray(ts_class2); ts_class2 = ts_class2.astype(np.float)
    class1_ts_all=[]
    class2_ts_all=[]
    for i in range(sample_multiplier):
        np.random.seed(seed=i)
        noisy_ts = np.random.normal(np.mean(ts_class1), np.std(ts_class1), len(ts_class1))
        alpha = calc_alpha(target_d_idx,ts_class1,ts_class2,noisy_ts)
        print alpha
    #print "alpha=",alpha,args[0]
    #print "mean and std of ts_class1,2 before adding noise", np.mean(ts_class1),np.mean(ts_class2), np.std(ts_class1), np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    #noisy_ts = np.random.normal(np.mean(ts_class1), np.std(ts_class1), len(ts_class1))
        ts_class1_wn = ts_class1 + alpha*noisy_ts
        class1_ts_all.append(ts_class1_wn)
    #print np.sum(np.multiply(alpha,noisy_ts))
        ts_class2_wn = ts_class2 + alpha*noisy_ts
        class2_ts_all.append(ts_class2_wn)
    #print "mean and std of ts_class1,2 after adding noise", np.mean(ts_class1),np.mean(ts_class2), np.std(ts_class1), np.std(ts_class2),np.mean(ts_class1)-np.mean(ts_class2)
    print len(class1_ts_all),len(class2_ts_all)
    class1_ts_all=[item for sublist in class1_ts_all for item in sublist]
    class2_ts_all=[item for sublist in class2_ts_all for item in sublist]
    #print len(class1_ts_all)
    d_idx_final = (np.mean(class1_ts_all)-np.mean(class2_ts_all))**2/(0.5*(np.std(class1_ts_all)**2+np.std(class2_ts_all)**2))
    ts_id = args[0].strip().split(".")[0:4]
    if float(args[1]).is_integer():
        ts_id.append('alpha'+str(int(args[1])))
    else:
        ts_id.append('alpha'+str(float(args[1])))
    ts_id.append('ts')
    ts_id = '.'.join(ts_id)
    print ts_id, d_idx_final, alpha
    writeTestStats(class1_ts_all,class2_ts_all,outfile)

main(sys.argv[1:])
