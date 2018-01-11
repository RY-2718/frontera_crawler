# Scrapy On Frontera
Scrapy + Fronteraを用いてクローリングするspiderです．

## 依存
- [Scrapy](https://github.com/scrapy/scrapy)
- [Frontera](https://github.com/scrapinghub/frontera)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache HBase](https://hbase.apache.org/)
- [Twisted Python](https://twistedmatrix.com/trac/)
    - ちょっと編集が必要

## 導入
### pythonでの依存パッケージの導入
fronteraの導入で変なことをしているのは依存を解決しつつGitHubのmasterリポジトリを取得するためです．

```
$ pip install scrapy colorlog msgpack-python frontera[distributed,kafka,hbase]
$ pip uninstall frontera
$ pip install pip install git+https://github.com/scrapinghub/frontera.git
```

### 設定ファイルの編集
scrapyの動作に関する設定は `/crawler/settings.py` に，fronteraに関する設定は `/frontier/common.py` ， `/frontier/\*\_settings.py` に記述してあります．
最低限設定すべき項目を以下に列挙します．

#### /frontier/common.py
```
SPIDER_FEED_PARTITIONS
SPIDER_LOG_PARTITIONS

KAFKA_LOCATION
SPIDER_LOG_DBW_GROUP
SPIDER_LOG_SW_GROUP
SCORING_LOG_DBW_GROUP
SPIDER_FEED_GROUP
SPIDER_LOG_TOPIC
SPIDER_FEED_TOPIC
SCORING_LOG_TOPIC
```

#### /frontier/\*\_settings.py
```
HBASE_THRIFT_PORT = 9090
HBASE_THRIFT_HOST = 'localhost'
HBASE_METADATA_TABLE = 'metadata'
HBASE_QUEUE_TABLE = 'queue-for'
```

### Kafka, HBaseの設定
Kafkaを導入，トピック（`SPIDER_LOG_TOPIC, SPIDER_FEED_TOPIC, SCORING_LOG_TOPIC`）を作成してください．

また，HBaseを導入し，`crawler` というnamespaceを作成してください．

### TODO
- `crawler/pipelines.py` の削除
- S3 bucketを `crawler/settings.py` で指定できるようにする
- twistedについての記述を増やす，もしくはsubpackage化
