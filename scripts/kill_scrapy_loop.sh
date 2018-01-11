#!/bin/bash

if [ $# -ne 1 ]; then
  echo "usage: bash $0 PARTITION_ID"
  exit 1
fi

# show header
ps alx | head -1
#kill children
ps alx | grep python | grep "SPIDER_PARTITION_ID=$1"
ppid=`ps alx | grep python | grep "SPIDER_PARTITION_ID=$1" | awk '{print $4}'`
ps l -p $ppid

echo "really kill them? [Y/n]"
read ANSWER

ANSWER=`echo $ANSWER | tr y Y | tr -d '[\[\]]'`

case $ANSWER in
    ""|Y* ) 
        # get pid
        pid=`ps alx | grep python | grep "SPIDER_PARTITION_ID=$1" | awk '{print $3}'`
        ppid=`ps alx | grep python | grep "SPIDER_PARTITION_ID=$1" | awk '{print $4}'`
        # kill parent
        kill $pid
        #kill children
        kill $ppid;;
    *  ) echo "OK, I won't kill them.";;
esac
