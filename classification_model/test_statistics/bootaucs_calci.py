#! /usr/bin/python
from glob import glob
import numpy
from sys import exit, argv, stdout
import re
from numpy.random import random_integers
from Libroc import cvbmroc, pbmroc
from scipy import stats

def Resample(samps):
	num=len(samps)
	return samps[random_integers(low=0,high=num-1,size=num)]

def ComputeAUC(actually_neg, actually_pos):
	res=pbmroc(actually_neg,actually_pos)
	#print res
	return res[0],res[3]	


if len(argv) < 4:
	print """
usage: bootaucsCI.py nboot confidence_level outfile parfile1 [parfile2]
  This script uses bootstrap methods to generate nboot auc values for each
  input parameter file. The  input parameter files are in labroc4 format. 
  That is, they contain a group of text lines that are ignored, 
  a line containing 'large', and a group of rating values, followed by a
  line starting with '*', followed by more rating values, followed by a
  line starting with a '*'. It is assumed that the labroc4 data are in
  'large' organization, i.e., large values corresponding to actually
  present defects. The actually negative cases should come first followed
  by the actually positive cases. Also, unlike labroc4, it is required
  that each rating value be on a separate line.

  The rating values are resampled with replacement nboot times
  and the ROC fitting is applied to each set of sample ratings. The AUC value
  from each of the samples is then written to outfile in the format:
  parfile\tsampnum\taucval where sampnum is the bootstrap sample number
  going from 1 to nboot and aucval is the auc value obtained from labroc4.

  The script currently uses the UC ROCKit libroc.so library and the Libroc.py
  wrapper. These must be installed somewhere that python can find them
  (e.g. in the directory pointed to by your python path variable PYTHONPATH).
  If you use the python in the cluster in /mip/opt/bin64 it should just work.
"""
	exit(1)

nsamp=int(argv[1])
outf=open(argv[3],'w')
outf.write("name\tsamp\tauc\n")
cl=int(argv[2])
for f in argv[4:]:
	inf=open(f,'r')
	vals=[]
	# skip header. Read until we find 'large'
	while True:
		l=inf.readline()
		l=l.strip()
		if l.lower() == 'large':
			break
	if l != 'large':
		print "missing 'large' in",f
		exit(1)
	# read actually negative values
	while True:
		l=inf.readline()
		l=l.strip()
		if l[0] == '*':
			break
		vals.append(float(l))
	if l[0] != '*':
		print "missing *"
		exit(1)
	nl=numpy.array(vals)

	#read actually positive values
	vals=[]
	while True:
		l=inf.readline()
		l=l.strip()
		if l[0] == '*':
			break
		vals.append(float(l))
	inf.close()
	if l[0] != '*':
		print "missing *"
		exit(1)
	wl=numpy.array(vals)
	aucs=[]

	#print f, nl.mean(), nl.shape[0], wl.mean(), wl.shape[0], 
	stdout.flush()
	newaucs=[]
	for isamp in range(0,nsamp):
		nl_resamp=Resample(nl)
		wl_resamp=Resample(wl)
		res=ComputeAUC(nl_resamp,wl_resamp)
		aucs.append(res[0])
		outf.write("%s\t%d\t%f\n" % \
						(f, isamp,aucs[-1]))
	aucs=numpy.array(aucs)
	countLevel=f.split('.')[1].strip()[2:]
	#print  'auc mean,std:', aucs.mean(), aucs.std()
outf.close()
#std_error = aucs.std()/(nsamp**0.5)
std_error = aucs.std()
alpha = 1 - (cl/100.0)
p = 1 - (alpha/2)
dof = nsamp - 1
criticalValue = stats.norm.ppf(p)
marginal_error = criticalValue * std_error
lower_bound =aucs.mean()-marginal_error
upper_bound =aucs.mean()+marginal_error 
#print "%s  %s percent confidence interval: %s %s %s " %(f, cl, countLevel ,lower_bound ,upper_bound)
#print "%s  %s percent CI error and sample mean: %s %s %s " %(f, cl, countLevel ,marginal_error ,aucs.mean())
print aucs.mean(),marginal_error,f

