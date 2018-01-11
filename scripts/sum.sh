#!/bin/bash

cd `dirname $0`

#j=`cat ../log/last-crawled.log | awk '{m += $6} END {print m;}'`
#echo "j=$j"
#k=`cat ../log/scrapy.log  | grep Crawled | tail -1 | awk '{print $6}'`
#echo "k=$k"
#s=`expr $i + $j + $k`
j=`zcat ../urls/archive/urls.log* | wc -l | awk '{print $1}'`
echo "j=$j"
k=`wc -l ../urls/urls.log | awk '{print $1}'`
echo "k=$k"
s=`expr $j + $k`
echo "s=$s"
