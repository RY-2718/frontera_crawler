#!/bin/bash

cd `dirname $0`

if [ $# = 1 ]; then
  i=$1
else
  i=1000
fi

tail -$i ../urls/urls.log | sed -e "s/http:\/\///" -e "s/https:\/\///" | sed -e "s/....-..-.. ..:..:..,... \([a-z0-9.-]*\).*/\1/" | sort | uniq -c | sort -n | awk '{if ($1 >= 10) print $0}'
