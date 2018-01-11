#!/bin/bash

# kill parents
ps aux | grep python | grep config | grep worker_settings | awk '{print $2}' | xargs ps l | awk 'NR>1 {print $4}' | xargs ps
#kill children
ps aux | grep python | grep config | grep worker_settings

echo "really kill them? [Y/n]"
read ANSWER

ANSWER=`echo $ANSWER | tr y Y | tr -d '[\[\]]'`

case $ANSWER in
    ""|Y* )
        # kill parents
        ps aux | grep python | grep config | grep worker_settings | awk '{print $2}' | xargs ps l | awk 'NR>1 {print $4}' | xargs kill
        #kill children
        ps aux | grep python | grep config | grep worker_settings | awk '{print $2}' | xargs kill ;;
    *  ) echo "OK, I won't kill them.";;
esac

