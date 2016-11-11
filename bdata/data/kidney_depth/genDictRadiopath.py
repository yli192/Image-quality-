#! /usr/bin/python
import sys
import collections
import pickle
def nested_dict():
    return collections.defaultdict(nested_dict)
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def read_aveatncoeff(datafile , d):
    infile = open(datafile)
    infile.seek(0)
    for line in infile:
        line = line.strip().split(" ")
        mean_atn_coeff = line[1]
        phanbase = line[0].split(".")[0]
        age = phanbase[0:2]
        gender = phanbase[2]
        if phanbase[3] == 'R':
            hp =phanbase[3:6]
            ks = phanbase[6:]
            if not ks:
                ks = 'normal'
        else:
            hp = phanbase[3:5]
            ks = phanbase[5:]
            if not ks:
                ks = 'normal'

        d[age][gender][hp][ks]['ave_atncoeff']=mean_atn_coeff
    return d

def read_anttopos (datafile, d):
    infile = open(datafile)
    infile.seek(0)
    for line in infile:
        line = line.strip().split(" ")
        anterior_atnsum = line[1]
        posterior_atnsum = line[2]
        age = line[0][0:2]
        gender = line[0][2]
        if line[0][3] == 'R':
            hp = line[0][3:6]
            ks = line[0][6:]
            if not ks:
                ks = 'normal'
        else:
            hp = line[0][3:5]
            ks = line[0][5:]
            if not ks:
                ks = 'normal'
        #print age,gender,hp,ks,defloc
        d[age][gender][hp][ks]['anterior_atncoeffsum']=anterior_atnsum
        d[age][gender][hp][ks]['posterior_atncoeffsum']=posterior_atnsum
    return d

def main(args):
    if (len(args) != 2):
        print "Arguments: datafile1 datafile2"
        exit();
    d = nested_dict() #initialize d
    #for i in range(len(args)):
    #    d = read_defcontrast(args[i],d)
    d = read_anttopos(args[0],d)
    d = read_aveatncoeff(args[1],d)
    save_obj(d, 'radiopathdict' )
    print d['10']['F']['10']['n15'] # check; should be equal to 871
main(sys.argv[1:])
