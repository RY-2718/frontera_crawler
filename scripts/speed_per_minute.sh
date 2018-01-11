#!/bin/bash

cd `dirname $0`

v=`cat ../scrapy_log/scrapy.log | grep Crawled | head -1 | awk '{print $1 "_" $2 " " $6}'`
w=`cat ../scrapy_log/scrapy.log | grep Crawled | tail -1 | awk '{print $1 "_" $2 " " $6}'`
python ../scripts/py/speed_per_minute.py $v $w
