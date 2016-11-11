#! /mip/opt/bin/python
'''
    Filename: plotErrorbar.py
    Author: Gary Li
    Date: June 2016
    Latest Revision
    Python Version: 2.7
    Program Name: plotauc
    Usage: plotauc aucfile
    this code reads in the first and second column of a text file and plots the mean AUC values (1st column) and its confidence intervals (2nd column) against % injected activity using the matplotlib.pyplot.scatter & matplotlib.pyplot.errorbar function
'''

import sys
import matplotlib.pylab as plt
import numpy as np

def plterrorbar(auc_file):
 colors = "gry"
 color_index=0
 for x in ['10','50','90']:
  print x
  mean_aucs=[]
  marginal_error=[]
  count_levels=[]
  auc_file.seek(0)
  for line in auc_file:
       line = line.strip().split()
       print line
       filename = line[2]
       heightp = "hp" + x
       if filename.split('.')[1] == heightp:
	mean_aucs.append(float(line[0]))
	count_levels.append(float(filename.split('.')[2][2:]))
	marginal_error.append(float(line[1]))
  print mean_aucs,marginal_error,count_levels
  plt.scatter(count_levels,mean_aucs,c=colors[color_index],label=heightp)
  plt.errorbar(count_levels,mean_aucs,yerr=marginal_error,c=colors[color_index], linestyle="None")
  color_index += 1


def main(args):
 mean_aucs=[]
 marginal_error=[]
 count_levels=[]

 if (len(args) != 1):
	print "Arguments: datafile"
	exit();

 auc_file = open(args[0])
 plterrorbar(auc_file)
 plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, bbox_to_anchor=(0.6, 0.8))
 plt.ylim([0,1])
 plt.xlabel('% injected activity')
 plt.ylabel('Mean AUC values generated using bootstrapping')
 plt.show()

main(sys.argv[1:])
