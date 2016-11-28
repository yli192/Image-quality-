#!/bin/bash

FAIL=0

echo "starting"

./sleeper.pl 2 0 &
./sleeper.pl 2 1 &
./sleeper.pl 3 0 &
./sleeper.pl 10 0 &


#ps -u gary

#given a pid, wait on the pid
#PID=8374
#while ps -p $PID; do sleep 1; done


#for job in `jobs -p`
#  do
#    echo $job
#    #wait $job || let "FAIL+=1"
#done



#fin dou current working directory of a running process:
#pwdx $PID
