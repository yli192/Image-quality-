#! /usr/bin/python
import sys
import pickle
import collections
import matplotlib.pyplot as plt
import numpy as np
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
    #print ("The mean of %i %s in %s is %f "% (len(key_list1),key[-1],key[0:-1],ave))
    return ave

def calc_stats_defvol_dict(dict,key):
    key_list=[]
    #print key
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
    #print ("The mean of %i %ss in %s is %f "% (len(key_list2),key[-1],key[0:-1],ave))
    return ave

def calc_stats_auc_dict(dict,key):
    #print key
    #for item in key:
    #    print item
    item_value=dict[key[0]][key[1]][key[2]][key[3]][key[4]]
    #print ("The AUC value for %s is %s " % (key,item_value))
    return item_value

def replace(original_key,replace_index,replace_string):
    new_key= [None] * len(original_key)
    for idx,val in enumerate(original_key):
        #print idx,val
        if idx == replace_index:
            new_key[idx]=replace_string
        else:
            new_key[idx]=original_key[idx]
    return new_key

def main(args):
    if (len(args) != 3 ):
        print "Arguments: auc_key kid_depth_key defvol_key \n"
        print  "auc_key sample: d['00']['50']['100']['12']; age, hp, count level, cutoff \n"
        print  "Kid_depth_key sample: d['10']['F']['10']['n15']['anterior_atncoeffsum'] or ['posterior_atncoeffsum']; age, gender, hp, ks, anterior or posterior  \n"
        print  "defvol_dict_key sample: d['10']['F']['10']['normal']['lat']['actual_contrast' or 'actual_defvol' or 'target_contrast' or 'target_defvol'] ;hp:10,Ref,90\n"
        exit();
    auc_key = args[0].strip().split(',')
    kid_depth_key = args[1].strip().split(',')
    defvol_key = args[2].strip().split(',')
    print ("keys entered:\n auc_key:%s \n kid_depth_key:%s \n defvol_key:%s \n "%(auc_key, kid_depth_key, defvol_key))
    dict1='./defvoldict.pkl'
    dict2='./radiopathdict.pkl'
    dict3='./aucdict.pkl'
    defvol_dict = load_obj(dict1)
    kid_depth_dict = load_obj(dict2)
    auc_dict = load_obj(dict3)
#auc, construct key for hp50 and 90, given 10
    auc_list = []
    auc =calc_stats_auc_dict(auc_dict,auc_key)
    auc_list.append(auc)
    auc_key_hp50 = replace(auc_key,1,'50') #original_key,replace_index,replace_string
    auc_hp50 =calc_stats_auc_dict(auc_dict,auc_key_hp50)
    auc_list.append(auc_hp50)
    auc_key_hp90 = replace(auc_key,1,'90')
    auc_hp90 =calc_stats_auc_dict(auc_dict,auc_key_hp90)
    auc_list.append(auc_hp90)
    #auc_list_arr = np.array (auc_list)
    #auc_list_std = np.std(auc_list_arr)
    #print "auc_list_std:",auc_list_std

#atncoeff_mean, construct key for hp50 and 90, given 10
    atncoeff_mean_list = []
    atncoeff_mean = calc_stats_kid_depth_dict(kid_depth_dict,kid_depth_key)
    atncoeff_mean_list.append(atncoeff_mean)
    kid_depth_key_hp50 = replace(kid_depth_key,2,'Ref')
    atncoeff_mean_hp50 = calc_stats_kid_depth_dict(kid_depth_dict,kid_depth_key_hp50)
    atncoeff_mean_list.append(atncoeff_mean_hp50)
    kid_depth_key_hp90 = replace(kid_depth_key,2,'90')
    atncoeff_mean_hp90 = calc_stats_kid_depth_dict(kid_depth_dict,kid_depth_key_hp90)
    atncoeff_mean_list.append(atncoeff_mean_hp90)
    atncoeff_mean_arr = np.array (atncoeff_mean_list)
    atncoeff_mean_std = np.std(atncoeff_mean_arr)
    print "atncoeff_mean_std:",atncoeff_mean_std

#defcontrast_mean, construct key for hp50 and 90, given 10
    defcontrast_mean_list = []
    defcontrast_mean = calc_stats_defvol_dict(defvol_dict,defvol_key)
    defcontrast_mean_list.append(defcontrast_mean)
    defvol_key_hp50 = replace(defvol_key,2,'Ref')
    defcontrast_mean_hp50 = calc_stats_defvol_dict(defvol_dict,defvol_key_hp50)
    defcontrast_mean_list.append(defcontrast_mean_hp50)
    defvol_key_hp90 = replace(defvol_key,2,'90')
    defcontrast_mean_hp90 = calc_stats_defvol_dict(defvol_dict,defvol_key_hp90)
    defcontrast_mean_list.append(defcontrast_mean_hp90)
    defcontrast_mean_arr = np.array (defcontrast_mean_list)
    defcontrast_mean_std = np.std(defcontrast_mean_arr)
    print "defcontrast_mean_std:",defcontrast_mean_std
    #print auc_list,atncoeff_mean_list,defcontrast_mean_list
#plot auc
    height_percentile=[10,50,90]
    plt.figure(1)
    plt.plot(height_percentile,auc_list , 'ro')
    plt.xlabel('height_percentile')
    plt.ylabel('AUC values')
    auc_tilte= replace(auc_key,1,'*')
    plt.title('AUC values of %s' %auc_tilte)
    plt.axis([0, 100, 0.5, 1])
    #plt.show()
#plot atncoeff_mean
    plt.figure(2)
    plt.plot(height_percentile,atncoeff_mean_list , 'ro')
    plt.xlabel('height_percentile')
    plt.ylabel('average of atncoeffs ')
    kid_depth_tilte= replace(kid_depth_key,2,'*')
    plt.title('Atncoeff averages of %s' %kid_depth_tilte)
    plt.axis([0, 100, min(atncoeff_mean_list)*0.8, max(atncoeff_mean_list)*1.2])
#plot defcontrast_mean
    plt.figure(3)
    plt.plot(height_percentile,defcontrast_mean_list , 'ro')
    plt.xlabel('height_percentile')
    plt.ylabel('average of defcontrasts ')
    defvol_key_tilte= replace(defvol_key,2,'*')
    plt.title('Defcontrasts averages of %s' %defvol_key_tilte)
    plt.axis([0, 100, min(defcontrast_mean_list)*0.8, max(defcontrast_mean_list)*1.2])
    plt.show()

#calculate statistics
    #ant_atncoeff_key = ['05','*','10','*','anterior_atncoeffsum'] #age,gender,hp,ks,ant_or_pos

    #pos_atncoeff_key = ['05','*','10','*','posterior_atncoeffsum'] #age,gender,hp,ks,ant_or_pos
    #pos_atncoeff_mean = calc_stats_kid_depth_dict(kid_depth_dict,pos_atncoeff_key)

    #defcontrast_key = ['05','*','10','*','*','actual_contrast']

    #defvol_key = ['05','*','10','*','*','actual_defvol']
    #defvol_mean = calc_stats_defvol_dict(defvol_dict,defvol_key)

    #auc_key = ['05','10','100','12','AUC']


main(sys.argv[1:])
