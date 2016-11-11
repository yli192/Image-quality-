#!  /mip/opt/bin/python
from runcmd import runcmd, waitall
import csv
import numpy as np
import random
import os
import sys
if (len(sys.argv[1:]) != 3):
   print "Arguments: num_uptakeRealizations phantom_bindir csv_dir"
   print "Sample arguments: 192 /netscratch/garyli/uf/phantom/dir2/ /netscratch/garyli/im_quality/csv/csv_192urs_a00only/"
   exit();
#defloc=1 #1=no def,2=upper pole,4=lateral,3=lower pole
num_urs=int(sys.argv[1])
datadir=sys.argv[2]
csvdir=sys.argv[3]
numNoDefUrs=num_urs/2 # number of defect-free uptake realizations
numUpDefUrs=numNoDefUrs+num_urs/6 # number of upper pole defect uptake realizations
numLatDefUrs=numUpDefUrs+num_urs/6  # number of later defect uptake realizations
numLowDefUrs=numLatDefUrs+num_urs/6 # number of lower pole defect uptake realizations
kliv = 0.043 # fraction of activity went to the liver, fixed
kspl = 0.017 # fraction of activity went to the spleen, fixed
kwashout = 0.018 # fraction of activity due to biological washout
#datadir = '/netscratch/garyli/uf/phantom/dir1/'
#csvdir= '/netscratch/garyli/im_quality/csv/csv_'+sys.argv[1]+'urs/'
for i in [0.25, 0.5, 0.75, 1, 1.25, 1.5]:
 percent_inj = float(i)
 CsvFile=[csvdir,int(percent_inj*100),'.csv']
 csvfile=["".join([str(i) for i in CsvFile])]
 with open(csvfile[0],'rU') as csvread:
     reader=csv.reader(csvread,delimiter=',',lineterminator='\n')
     reader.next()
     for row in reader:
        kbkg=1-kliv-kspl-kwashout-float(row[8])	
        cwd = os.getcwd()
        #print cwd
        RD=[cwd,'/',int(percent_inj*100),'/',row[2],'/',row[4],'/']
        rd="".join([str(i) for i in RD])
        if int(row[0]) < numNoDefUrs+1: #sorting based on numNoDefUrs, here use the first half urs for defect-free urs
 	 FILE=[rd,'sprj.','ur',int(row[0]),'.',row[1],'.im']
 	 file= "".join([str(i) for i in FILE])
 	 if os.path.exists(file) is not True:
 	  #print file
           CMD=['./sprj_cv.py',' ',row[1],' ',round(float(row[7]),3),' ',round(float(row[8]),3),' ',round(kliv,3),' ',round(kspl,3),' ',round(float(row[9]),3),' ',1920,' ',1,' ',rd,'sprj.','ur',int(row[0]),'.',row[1],'.im','>>',rd,row[1],'.log',' ','2>&1']
           cmd="".join([str(i) for i in CMD])
           runcmd(cmd,maxruns=32,rundir=cwd,waittime=2,debug=True)
        elif int(row[0]) > numNoDefUrs and int(row[0]) < numUpDefUrs+1:  
 	 FILE=[rd,'sprj.','ur',int(row[0]),'.',row[1],'.im']
         file= "".join([str(i) for i in FILE])
         if os.path.exists(file) is not True:
 	  #print file
 	   UPCMD=['./sprj_cv.py',' ',row[1],' ',round(float(row[7]),3),' ',round(float(row[8]),3),' ',round(kliv,3),' ',round(kspl,3),' ',round(float(row[9]),3),' ',1920,' ',2,' ',rd,'sprj.','ur',int(row[0]),'.',row[1],'.im','>>',rd,row[1],'.log',' ','2>&1']
           upcmd="".join([str(i) for i in UPCMD])
 	   runcmd(upcmd,maxruns=32,rundir=cwd,waittime=2,debug=True) 
        elif int(row[0]) > numUpDefUrs and int(row[0]) < numLatDefUrs+1:  
 	  FILE=[rd,'sprj.','ur',int(row[0]),'.',row[1],'.im']
          file= "".join([str(i) for i in FILE])
          if os.path.exists(file) is not True:
 	   #print file
            LATCMD=['./sprj_cv.py',' ',row[1],' ',round(float(row[7]),3),' ',round(float(row[8]),3),' ',round(kliv,3),' ',round(kspl,3),' ',round(float(row[9]),3),' ',1920,' ',4,' ',rd,'sprj.','ur',int(row[0]),'.',row[1],'.im','>>',rd,row[1],'.log',' ','2>&1']
            latcmd="".join([str(i) for i in LATCMD])
 	    runcmd(latcmd,maxruns=32,rundir=cwd,waittime=2,debug=True) 
        elif int(row[0]) > numLatDefUrs and int(row[0]) < numLowDefUrs+1:
 	   FILE=[rd,'sprj.','ur',int(row[0]),'.',row[1],'.im']
 	   file= "".join([str(i) for i in FILE])
 	   if os.path.exists(file) is not True:
 	    #print file
             LOWCMD=['./sprj_cv.py',' ',row[1],' ',round(float(row[7]),3),' ',round(float(row[8]),3),' ',round(kliv,3),' ',round(kspl,3),' ',round(float(row[9]),3),' ',1920,' ',3,' ',rd,'sprj.','ur',int(row[0]),'.',row[1],'.im','>>',rd,row[1],'.log',' ','2>&1']
 	     lowcmd="".join([str(i) for i in LOWCMD])
 	     runcmd(lowcmd,maxruns=32,rundir=cwd,waittime=2,debug=True) 
