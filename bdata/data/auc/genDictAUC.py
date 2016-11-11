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

def read_aucs(datafile,d):
    infile = open(datafile)
    infile.seek(0)
    for line in infile:
        line = line.strip().split(' ')
        auc = line[0]
        marginal_error = line[1]
        age = line[2].split('.')[0][1:]
        hp = line[2].split('.')[1][2:]
        cl = line[2].split('.')[2][2:]
        cf = line[2].split('.')[3][1:]
        d[age][hp][cl][cf]['AUC']=auc
        d[age][hp][cl][cf]['marginal_error']=marginal_error
    return d

def main(args):
    if (len(args) != 5):
        print "Arguments: datafile1 datafile2 datafile3 datafile4 datafile5"
        exit();

    d = nested_dict()
    for i in range(len(args)):
        d = read_aucs(args[i],d)
    print d['00']['50']['100']['12'] # age, hp, count level, cutoff
    save_obj(d,'aucdict')
main(sys.argv[1:])
