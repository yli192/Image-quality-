#! /bin/bash
#PID=8793
#while ps -p $PID; do sleep 1; done
#new job
#echo "wait finishes, new job starts"


while pgrep -u gary r > /dev/null; do sleep 1; done
    echo "new job starts"
