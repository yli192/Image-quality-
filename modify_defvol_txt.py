#! /usr/bin/python
import sys

def changeDefvol(infile,outfile):
    line_num = 0
    w = open(outfile,'w')
    for line in infile:
        line = line.strip().split(' ')
        hp = line[2][1:3]
        if (hp == "Re"):
            hp10 = ' '.join([line[0],line[1],line[2][0]+"10"+line[2][4:],line[3]])
            hp90 = ' '.join([line[0],line[1],line[2][0]+"90"+line[2][4:],line[3]])
            hp50 = ' '.join(line)
            w.write(hp10+'\n')
            w.write(hp50+'\n')
            w.write(hp90+'\n')
            w.close
    #print dict_std


def main(args):
    if (len(args) != 2):
        print "Arguments: infile outfile"
        exit();
    infile = open(args[0])
    outfile = args[1]
    changeDefvol(infile,outfile)

main(sys.argv[1:])
