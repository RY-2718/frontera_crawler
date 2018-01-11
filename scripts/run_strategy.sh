#!/bin/bash

cd `dirname $0`
cd ..

while :
do
    python frontier/run_strategy.py --config worker_settings --partition-id 0
    echo -e "\n\n"
    echo "--------------------restart!--------------------"
    echo "stopped strategy worker at" `date +"%Y/%m/%d %T"` >> "frontera_log/restart_worker.log"
done
