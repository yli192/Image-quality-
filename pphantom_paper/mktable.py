#! /mip/opt/bin/python
import sys
import csv
def get_defvol(defvol_file):
	"""Get the defect volume of a phantom per defect location """
	
	defvol_file.seek(0)
	d = {}
	c = {}
	for line in defvol_file:
	    #print line
	    defvol = line.strip().split()[0]
	    age = line.strip().split()[1]
	    phanbase = line.strip().split()[2]
	    defloc = line.strip().split()[3]	
	    key = age + phanbase
	    #d[key]= defloc+":"+defvol
	    c[defloc] = defvol
	    d[key]= defloc
	    #c[defloc] = defvol
	    d[key] = c
	    c = {}
	#print d
	#return defvol,age,phanbase,defloc     
	return d
def get_data(data):
	e ={}
	f = {}
	"""Get data from a two column text file """
	for line in data:
		#print line
		value = line.strip().split(',')[0]
		key = line.strip().split(',')[1]
		marker = line.strip().split(',')[2]
	        f[marker]=value
		e [key] = marker
		e [key] = f
		f = {}
	return e

def dict_update(dict1,dict2):
	"""Concatenate items unders common keys in input dictionaries """
	for key1 in dict1:
	  for key2 in dict2:
		if key1 == key2:
			dict1[key1].update(dict2[key2])
	return dict1

def main(args):
	
	if (len(args) != 13):
		print "Arguments: Defvol_file1 Defvol_file2 Defvol_file3 Defvol_file4 Defvol_file5 Defvol_file6 height_file weight_file mrr_file thickness_file1 thickness_file2 thickness_file3 kidneysize_file"
		exit();
	defvol_file_0 = open(args[0])
	defvol_file_1 = open(args[1])
	defvol_file_2 = open(args[2])
	defvol_file_3 = open(args[3])
	defvol_file_4 = open(args[4])
	defvol_file_5 = open(args[5])
	height_file = open(args[6])
	weight_file = open(args[7])
	mrr_file = open(args[8])
	thickness_lp_file = open(args[9])
	thickness_up_file = open(args[10])
	thickness_lat_file = open(args[11])
	ks_file = open(args[12])
	
	#num_lines = sum(1 for line in defvol_file)
	#print num_lines
	#for i in range(num_lines):
	#	print i
	#(defvol,age,phanbase,defloc) = get_defvol(defvol_file)
	d1 = get_defvol(defvol_file_0)
	d2 = get_defvol(defvol_file_1)
	d3 = get_defvol(defvol_file_2)
	d4 = get_defvol(defvol_file_3)
        d5 = get_defvol(defvol_file_4)
        d6 = get_defvol(defvol_file_5)
	d12 = dict_update(d1,d2)
	d123 = dict_update(d12,d3)
	d45 = dict_update(d4,d5)
        d456 = dict_update(d45,d6)
	#print d1,'\n',d2,'\n',d3
	d123456 = d123.update(d456)
	#print len(d123.keys()),d123
	hd = get_data(height_file)
	wd = get_data(weight_file)
	mrrd = get_data(mrr_file)
	ksd = get_data(ks_file)
	lattd = get_data(thickness_lat_file)
	uptd = get_data(thickness_up_file)
	lptd = get_data(thickness_lp_file)
	d123h=dict_update(d123,hd)
	d123hw=dict_update(d123h,wd)
	d123hwmrr=dict_update(d123hw,mrrd)
	d123hwmrrks=dict_update(d123hwmrr,ksd)
	d123hwmrrkslatt=dict_update(d123hwmrrks,lattd)
	d123hwmrrkslattupt=dict_update(d123hwmrrkslatt,uptd)
	d123hwmrrkslattuptlpt=dict_update(d123hwmrrkslattupt,lptd)
	#d123.update(wd)
	#d123.update(mrrd)
	#print d123hwmrrkslattuptlpt
#	writer = csv.writer(open('table.csv','wb'))
#	for key in d123hwmrrkslattuptlpt.keys():
#		writer.writerow([key])
#		for key,value in d123hwmrrkslattuptlpt[key].items():
#			writer.writerow([key,value]) 
	print "phanbase\tweight(kg)\theight(cm)\tmean_radius_rotation(cm)\tlateral_cortex_thickness(cm)\tupperpole_cortex_thickness(cm)\tlowerpole_cortex_thickness(cm)\tlateral_defect_volume(voxels[0.1^3cm^3])\tupperpole_defect_volume(voxels)\tlowerpole_defect_volume(voxels)\tkidney_volume(cm^3)"
	for key in d123hwmrrkslattuptlpt.keys():
		print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (key,d123hwmrrkslattuptlpt[key]['weight'],d123hwmrrkslattuptlpt[key]['height'],d123hwmrrkslattuptlpt[key]['mrr'],d123hwmrrkslattuptlpt[key]['lat_thickness'],d123hwmrrkslattuptlpt[key]['up_thickness'],d123hwmrrkslattuptlpt[key]['lp_thickness'],d123hwmrrkslattuptlpt[key]['lat'],d123hwmrrkslattuptlpt[key]['up'],d123hwmrrkslattuptlpt[key]['lp'],d123hwmrrkslattuptlpt[key]['kidneysize'])
	#print "%s\t%d\t%d\t%d\t%.2f\t%.3f\t%.3f\t%.3f\t%d\t%.4g\t%.4g" % (p,acqduration,numframes,duration,pixsize,xtalthick,collangres,kvoxels,ksum,activity,sens)


	defvol_file_1.close()
	defvol_file_2.close()
	defvol_file_3.close()
	defvol_file_4.close()
	defvol_file_5.close()
	defvol_file_0.close()

main(sys.argv[1:])
