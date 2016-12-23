#! /usr/bin/python
import sys

def changeDefvol(infile,outfile):
    line_num = 0
    for line in infile:
        line = line.strip().split(' ')
        hp = line[2][1:3]
        if (hp == "Re"):
            print line


def main(args):
    if (len(args) != 2):
        print "Arguments: infile outfile"
        exit();
    infile = open(args[0])
    outfile = args[1]
    changeDefvol(infile,outfile)

main(sys.argv[1:])
