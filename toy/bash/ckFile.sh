#! /bin/bash

current_dir_fullpath=${PWD}
num_files=`ls $current_dir_fullpath/*.py | wc -l` 

if [ $num_files != '2' ]; then
    echo $num_files
fi


#loop over files in a dir
for f in $current_dir_fullpath/*.sh
    do
     echo "Processing $f"
          # do something on $f
     done


#find file that ends w/ .log and delete them if they are smaller than 10k or use +10k if they are greater than 10k ,and use -at -10k if they are equal to 10k
find . -name "*.log" -size -10k -delete
