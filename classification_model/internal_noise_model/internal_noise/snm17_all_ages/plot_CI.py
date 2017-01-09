#! /usr/bin/python
import sys
import matplotlib.pylab as plt
import itertools

def main(args):
        if(len(args) != 1):
                print "Arguments: CI.txt"
                exit();

        ci_txt= open(args[0])
        mean_auc=[]
        marginal_error=[]
        HP=[]
        colors = "ryg"
        color_index=0
        marker = itertools.cycle(('o', 'v', '^', '<', '>', 's', '8', 'p'))
        for line in ci_txt:
                line = line.strip().split(" ")
                mean_auc.append(float(line[0]))
                marginal_error.append(float(line[1]))
                heightp=line[2].split(".")[1]
                hp=float(heightp[2:])
                HP.append(hp)
                plt.scatter(hp,float(line[0]),c=colors[color_index],marker=marker.next(),label=heightp)
                plt.errorbar(hp,float(line[0]),yerr=float(line[1]),c=colors[color_index],linestyle="None")
                print colors[color_index]
                color_index += 1


        #plt.legend(loc='upper left', numpoints=3, ncol=1, fontsize=16, bbox_to_anchor=(0.6, 1))
        plt.legend(loc='upper right', numpoints=1, ncol=3, fontsize=16)
        my_xticks = ['10', '50', '90']
        #x = np.array([10,50,90])
        plt.xticks(HP, my_xticks)
        plt.xlabel("Patient height percentile")
        plt.ylabel('Area under ROC curve')
        #plt.ylim((0.8,0.9))

        #plt.title(args[0])
        plt.show()


main(sys.argv[1:])
