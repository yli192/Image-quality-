#! /bin/bash


for i in 1 2 10
  do
    ./sleeper.pl $i 0 & 
done
wait #the wait here waits all processes(but not subprocesses spawned) in the forloop to finish 
echo 'loop finished'







