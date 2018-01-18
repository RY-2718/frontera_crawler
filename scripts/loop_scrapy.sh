#!/bin/bash

source /home/paul/workspace/venvs/scrapy-new/bin/activate

cd `dirname $0`
cd ..

if [ ! -f partition_id.txt ]; then
    echo "partition_id.txtにpartition idを書いておいてください"
    exit 1
fi
partition_id=`cat partition_id.txt | awk '{print $1}'`

# このスクリプトをkillした場合のため，再開時に同様の処理をかける
# 止まるまでに何ページcrawlしたかを残す
cat scrapy_log/scrapy.log | grep -a Crawled | tail -1 >> "log/last-crawled.log"

# urls/urls.logをローテーション
num=`ls urls/urls.log.* 2>/dev/null | wc -l`
if [ $num -ne 0 ]; then
    echo "mv urls/urls.log.* to urls/archive/"
    cat urls/urls.log.* | sed -e "s/http:\/\///" -e "s/https:\/\///" | sed -e "s/....-..-.. ..:..:..,... \([a-z0-9.-]*\).*/\1/" >> urls/for_making_list.txt
    gzip urls/urls.log.*
    mv urls/*.gz urls/archive/
fi

while : 
do
    # スクリプトによってscrapyがが動き始めることを標準出力から確認
    echo "scrapy (re)started at" `date +"%Y/%m/%d %T"`

    # scrapyを起動 なんらかの理由で停止した場合，以下の記録やローテーションなどを行う
    if [ partition_id = 0 ]; then
        scrapy crawl crawler -L INFO -s FRONTERA_SETTINGS=frontier.spider_settings -s SEEDS_SOURCE=seeds/list.txt -s SPIDER_PARTITION_ID=0
    else
        scrapy crawl crawler -L INFO -s FRONTERA_SETTINGS=frontier.spider_settings -s SPIDER_PARTITION_ID=$partition_id
    fi

    # 止まった時間を記録
    echo "scrapy stopped at" `date +"%Y/%m/%d %T"` >> "scrapy_log/restart_scrapy.log"

    # 止まるまでに何ページcrawlしたかを残す
    cat scrapy_log/scrapy.log | grep -a Crawled | tail -1 >> "scrapy_log/last-crawled.log"

    ## urls/urls.logをローテーション
    num=`ls urls/urls.log.* 2>/dev/null | wc -l`
    if [ $num -ne 0 ]; then
        echo "mv urls/urls.log.* to urls/archive/"
        cat urls/urls.log.* | sed -e "s/http:\/\///" -e "s/https:\/\///" | sed -e "s/....-..-.. ..:..:..,... \([a-z0-9.-]*\).*/\1/" >> urls/for_making_list.txt
        gzip urls/urls.log.*
        mv urls/*.gz urls/archive/
    fi
done
