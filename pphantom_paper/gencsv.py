#! /mip/opt/bin/python
import csv
import random
import os
import numpy as np
import scipy.stats as stats
from itertools import repeat
import glob
import sys
#percent_inj=1
if (len(sys.argv[1:]) != 2):
	print "Arguments: number_of_uptake_realizations phantom_bindir"
	print "Sample inputs: 192 /netscratch/garyli/uf/phantom/dir2/"
	exit();
num_samples = int(sys.argv[1])
datadir = sys.argv[2]
print num_samples
print datadir
countlevel=[0.25, 0.5, 0.75, 1, 1.25, 1.5]
#num_samples=48  # number of samples drawns from the normal distribution with parameterss specified above
#datadir = '/netscratch/garyli/uf/phantom/armsdown/'
mu_kact, sigma_kact = 0.361, 0.025 # mean and standard deviation of kact
mu_cratio, sigma_cratio = 1.68, 0.25 # mean and standard deviation of cratio
n=1.28 #n=1.28~80%, 1.64~90%, 2~95%
lower_kact, upper_kact = mu_kact-(n*sigma_kact), mu_kact+(n*sigma_kact)
lower_cratio, upper_cratio = mu_cratio-(n*sigma_cratio), mu_cratio+(n*sigma_cratio)
a= np.log(2)/(6.02*3600)# decay constant for Tc-99m
kact,cratio, pbase, sex, ages, heightpercentiles, bodymasses, ainj, atoi= ([] for i in range(9))
filenum = len(countlevel)*len(glob.glob1(datadir,"*.bin")) # two seed sequences are needed 1-540 and 541-1080 , num_files=90, num_countlevels=6
print filenum
counter=0
for percent_inj in countlevel:
 for file in os.listdir(datadir):
   if file.endswith(".bin"):
    counter=counter+1
    phanbase = file.split("_")
    basename = phanbase[0]
    print basename
    age = basename[0:2]
    gender = basename[2:3]
    if (basename[3:5] == "Re"):
         heightpercentile=50
    else:
           heightpercentile = basename[3:5]
   # print weightpercentile
    BodyMass = {'00M':3.5,'00F':3.4,'01M':10.4,'01F':9.5,'05M':20,'05F':20,'10M':30,'10F':35,'15M':55,'15F':50}
    BodyMassKey = [age, gender]
    bmk = "".join([str(v) for v in BodyMassKey])
    bodymass = BodyMass[bmk]
    Ainj = bodymass*0.05 # 0.05 mCi/kg according to the 2014 North American Guidelines
    if Ainj < 0.5:
         Ainj = 0.5
 	        #print "patient is too light, low AA bound is used"
    elif Ainj > 2.7:
         Ainj=2.7
 	        #print "patient is too heavy, high AA bound is used" 
    Ainj = Ainj * percent_inj
    #     print "count level=",percent_inj*100, "no correction made"
    print 'total injected activity=',Ainj
    Atoi=Ainj*np.exp(-a*10800) # imaging at 3 hrs after injection
 ###################################
    np.random.seed(seed=counter)
    print "seed#:",counter
    TotKidneyAct = stats.truncnorm.rvs((lower_kact-mu_kact)/sigma_kact,(upper_kact-mu_kact)/sigma_kact,loc=mu_kact,scale=sigma_kact,size=num_samples)
    #TotKidneyAct = np.random.normal(mu_kact, sigma_kact, num_samples)
    np.random.seed(seed=filenum+counter)
    print "seed#2:", filenum+counter
    Cratio = stats.truncnorm.rvs((lower_cratio-mu_cratio)/sigma_cratio,(upper_cratio-mu_cratio)/sigma_cratio,loc=mu_cratio,scale=sigma_cratio,size=num_samples)
    #Cratio = np.random.normal(mu_cratio,sigma_cratio,num_samples)
    kact.extend(TotKidneyAct)
    cratio.extend(Cratio)	  
    pbase.append(basename)
    sex.append(gender)
    ages.append(age)
    heightpercentiles.append(heightpercentile)
    bodymasses.append(bodymass)
    ainj.append(Ainj)
    atoi.append(Atoi)
 #duplicate lists
 #print ainj
 age_list=[x for item in ages for x in repeat(item,num_samples)]
 sex_list=[x for item in sex for x in repeat(item,num_samples)]
 pbase_list=[x for item in pbase for x in repeat(item,num_samples)]
 hp_list=[x for item in heightpercentiles for x in repeat(item,num_samples)]
 bm_list=[x for item in bodymasses for x in repeat(item,num_samples)]
 ainj_list=[x for item in ainj for x in repeat(item,num_samples)]
 #print ainj_list
 atoi_list=[x for item in atoi for x in repeat(item,num_samples)]
 ur_num=range(1,num_samples+1)*counter
 data=zip(ur_num,pbase_list,age_list,sex_list,hp_list,bm_list,ainj_list,atoi_list,kact,cratio)
 print percent_inj
 CsvName=[int(percent_inj*100),'.csv']
 csvname=["".join([str(i) for i in CsvName])]
 #print csvname[0]
 with open (csvname[0], 'wb',) as csvwrite:
   writer = csv.writer(csvwrite, delimiter=',',lineterminator='\n')
   title=['Ur#','Phanbase','Age','Sex','Height_percentile','Weight(Kg)','Injected activity','Activity at time of imaing','Kact','Cratio']
   writer.writerow(title)
   for i in data:
     #print i	
     writer.writerows([i])
 kact,cratio, pbase, sex, ages, heightpercentiles, bodymasses, ainj, atoi= ([] for i in range(9))
