#!/bin/bash

cd `dirname $0`
cd ..

while :
do
    python frontier/run_db.py --config worker_settings
    echo -e "\n\n"
    echo "--------------------restart!--------------------"
    echo "stopped db worker at" `date +"%Y/%m/%d %T"` >> "frontera_log/restart_worker.log"
done

