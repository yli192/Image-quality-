#! /bin/bash
ARGV1=$1
ARGV2=$2
#if [ -z "$ARGV" ]
if [ $# -ne 2 ]
    then 
        echo "Arguments: argv1 argv2"
        exit 1
else
    echo "The argvs you entered is: ${ARGV1:2:5} $ARGV2"
fi
echo "script continued; exit failed"


if [ -e 'cmdline_io.sh' ]
    then
        echo "exist"
fi

current_dir_fullpath=${PWD}
echo $current_dir_fullpath

#check if a directory exisis
if [ -d "$current_dir_fullpath" ]; then
    echo "$current_dir_fullpath exists"
fi
