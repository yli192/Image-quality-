#! /usr/bin/python
import sys

def readtxt(datafile):
    whole_dict = {}
    infile = open(datafile)
    infile.seek(0)
    for line in infile:
        lines = line.strip().split(" ")
        print lines
        phanbase = lines[1]+lines[2]
        print phanbase
        defvol_defloc = lines[-1]+"_defvol"
        print defvol_defloc
        defvol = lines[0]

        if phanbase in whole_dict:
            print "phanbase does exist"
        else:
            whole_dict[phanbase]={}

        whole_dict[phanbase][defvol_defloc] = defvol



    print whole_dict





def main(args):
    if (len(args) != 1):
        print "Arguments: datafile"
        exit();

    readtxt(args[0])

main(sys.argv[1:])
