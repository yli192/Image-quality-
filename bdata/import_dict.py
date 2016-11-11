#! /usr/bin/python
import sys
import pickle
import collections
#Nov 4, 2016
#Gary Y. Li
def nested_dict():
    return collections.defaultdict(nested_dict)

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open( name , 'rb') as f:
        return pickle.load(f)

def calc_stats_kid_depth_dict(dict,key):
    key_list=[]
    if (key[1] == '*'):
        for i in ['M','F']:
            key_i = [key[0],i,key[2],key[3],key[4]]
            key_list.append(key_i)

    key_list1=[]
    if (key[3] == '*'):
        for j in key_list:
            #print j
            for i in ['n15','normal','p15']:
                print
                updatedkey_i = [j[0],j[1],j[2],i,j[4]]
                key_list1.append(updatedkey_i)

    item_values =[]
    for item in key_list1:
        item_value=dict[item[0]][item[1]][item[2]][item[3]][item[4]]
        #print item,item_value
        item_values.append(float(item_value))

    ave = sum(item_values)/len(item_values)
    #print("Total score for %s is %s  " % (name, score))
    print ("The mean of %i %s in %s is %f "% (len(key_list1),key[-1],key[0:-1],ave))
    return ave

def calc_stats_defvol_dict(dict,key):
    key_list=[]
    if (key[1] == '*'):
        for i in ['M','F']:
            key_i = [key[0],i,key[2],key[3],key[4],key[5]]
            key_list.append(key_i)

    key_list1=[]
    if (key[3] == '*'):
        for j in key_list:
            #print j
            for i in ['n15','normal','p15']:
                #print
                updatedkey_i = [j[0],j[1],j[2],i,j[4],j[5]]
                key_list1.append(updatedkey_i)
            #remove j
    key_list2=[]
    if (key[4] == '*'):
        for j in key_list1:
            for i in ['up','lp','lat']:
    #            print
                updatedkey_i = [j[0],j[1],j[2],j[3],i,j[5]]
                key_list2.append(updatedkey_i)
    #key = []
    #print len(key_list1), key_list1
    item_values =[]
    for item in key_list2:
        item_value=dict[item[0]][item[1]][item[2]][item[3]][item[4]][item[5]]
        #print item,item_value
        item_values.append(float(item_value))

    ave = sum(item_values)/len(item_values)
    #print("Total score for %s is %s  " % (name, score))
    print ("The mean of %i %ss in %s is %f "% (len(key_list2),key[-1],key[0:-1],ave))
    return ave

def calc_stats_auc_dict(dict,key):
    #print key
    #for item in key:
    #    print item
    item_value=dict[key[0]][key[1]][key[2]][key[3]][key[4]]
    print ("The AUC value for %s is %s " % (key,item_value))

def main(args):
    if (len(args) != 3 ):
        print "Arguments: defvol_dict kid_depth_dict auc_dict"
        exit();
    #auc_key = args[0]
    #ant_atncoeff_key = args[1]
    #defcontrast_key = args[2]
    dict1=args[0]
    dict2=args[1]
    dict3=args[2]
    defvol_dict = load_obj(dict1)
    kid_depth_dict = load_obj(dict2)
    auc_dict = load_obj(dict3)
#calculate statistics
    #ant_atncoeff_key = ['05','*','10','*','anterior_atncoeffsum'] #age,gender,hp,ks,ant_or_pos
    ant_atncoeff_mean = calc_stats_kid_depth_dict(kid_depth_dict,ant_atncoeff_key)
    pos_atncoeff_key = ['05','*','10','*','posterior_atncoeffsum'] #age,gender,hp,ks,ant_or_pos
    pos_atncoeff_mean = calc_stats_kid_depth_dict(kid_depth_dict,pos_atncoeff_key)

    #defcontrast_key = ['05','*','10','*','*','actual_contrast']
    defcontrast_mean = calc_stats_defvol_dict(defvol_dict,defcontrast_key)
    defvol_key = ['05','*','10','*','*','actual_defvol']
    defvol_mean = calc_stats_defvol_dict(defvol_dict,defvol_key)

    #auc_key = ['05','10','100','12','AUC']
    auc =calc_stats_auc_dict(auc_dict,auc_key)

main(sys.argv[1:])
