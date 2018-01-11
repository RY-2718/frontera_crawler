#!/bin/bash

if [ $# -lt 1 ]; then
  echo "usage: bash $0 PARTITION_ID (domain_level)"
  exit 1
fi

cd `dirname $0`

cat ../urls/for_making_list.txt > /tmp/domains$1.txt
cat ../urls.log | sed -e "s/http:\/\///" -e "s/https:\/\///" | sed -e "s/....-..-.. ..:..:..,... \([a-z0-9.-]*\).*/\1/" >> /tmp/domains$1.txt

if [ $# = 2 ]; then
  # トップレベルから引数個だけドメインを見る
  cat /tmp/domains$1.txt | rev | cut -d. -f -$2 | rev | sort | uniq -c | sort -n | awk '{if ($1>=1000) print $1 " " $2}' > /tmp/candidate_with_count$1.txt
  cat /tmp/candidate_with_count$1.txt | awk '{print $2}' > /tmp/candidate$1.txt
  python ../scripts/py/make_list.py ../txt/blacklist.txt /tmp/candidate$1.txt
  rm /tmp/candidate$1.txt /tmp/candidate_with_count$1.txt
else
  # 引数が指定されなかった場合はドメインを切らずに見る
  cat /tmp/domains$1.txt | sort | uniq -c | sort -n | awk '{if ($1>=1000) print $1 " " $2}' > /tmp/candidate_with_count$1.txt
  cat /tmp/candidate_with_count$1.txt | awk '{print $2}' > /tmp/candidate$1.txt
  python ../scripts/py/make_list.py ../txt/blacklist.txt /tmp/candidate$1.txt
  rm /tmp/candidate$1.txt /tmp/candidate_with_count$1.txt
fi
