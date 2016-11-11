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

def read_defvol(datafile , d):
    infile = open(datafile)
    infile.seek(0)
    for line in infile:
        line = line.strip().split(" ")
        age = line[1]
        gender = str(line[2][0])
        if line[2][1] == 'R':
            hp = line[2][1:4]
            ks = line[2][4:]
            if not ks:
                ks = 'normal'
        else:
            hp = line[2][1:3]
            ks = line[2][3:]
            if not ks:
                ks = 'normal'
        defloc = line[-1]
        defvol = line[0]
        d[age][gender][hp][ks][defloc]=defvol
    return d

def read_defcontrast (datafile, d):
    infile = open(datafile)
    infile.seek(0)
    for line in infile:
        line = line.strip().split(" ")
        actual_contrast = line[0]
        target_contrast = line[1]
        actual_defvol = line[4]
        target_defvol = line[3]
        defloc = line[6]
        phanbase = line[7]
        age = line[7][0:2]
        gender = line[7][2]
        if line[7][3] == 'R':
            hp = line[7][3:6]
            ks = line[7][6:]
            if not ks:
                ks = 'normal'
        else:
            hp = line[7][3:5]
            ks = line[7][5:]
            if not ks:
                ks = 'normal'
        #print age,gender,hp,ks,defloc
        d[age][gender][hp][ks][defloc]['actual_contrast']=actual_contrast
        d[age][gender][hp][ks][defloc]['actual_defvol']=actual_defvol
        d[age][gender][hp][ks][defloc]['target_contrast']=target_contrast
        d[age][gender][hp][ks][defloc]['target_defvol']=target_defvol
    return d

def main(args):
    if (len(args) != 6):
        print "Arguments: datafile1 datafile2 datafile3 datafile4 datafile5 datafile6"
        exit();
    d = nested_dict() #initialize d
    for i in range(len(args)):
        d = read_defcontrast(args[i],d)
    save_obj(d,'defvoldict')
    print d['00']['F']['10']['normal']['lat'] # check; should be equal to 871
main(sys.argv[1:])
