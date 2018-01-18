# Scrapy On Frontera
Scrapy + Fronteraを用いてクローリングするプロジェクトです．

## 依存
- [Scrapy](https://github.com/scrapy/scrapy)
- [Frontera](https://github.com/scrapinghub/frontera)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache HBase](https://hbase.apache.org/)
- [Twisted Python](https://twistedmatrix.com/trac/)
    - docs/twisted-change.md に従って修正して下さい

## 導入
### pythonでの依存パッケージの導入
virtualenvなどで環境を切り分ける場合はよしなにやってください．
また，fronteraの導入で変なことをしているのは依存を解決しつつGitHubのmasterリポジトリを取得するためです．

```
$ pip install scrapy colorlog msgpack-python frontera[distributed,kafka,hbase]
$ pip uninstall frontera
$ pip install pip install git+https://github.com/scrapinghub/frontera.git
```

### 設定ファイルの編集
scrapyの動作に関する設定は `/crawler/settings.py` ，fronteraに関する設定は `/frontier/common.py` ， `/frontier/\*\_settings.py` ，ロギングに関する設定は `logging.conf` に記述してあります．
最低限設定すべき項目を以下に列挙します．

#### /crawler/settings.py
```
BUCKET_NAME # S3バケットの名前
```

#### /frontier/common.py
```
SPIDER_FEED_PARTITIONS # spider(Scrapy)の数
SPIDER_LOG_PARTITIONS # worker(Frontera)の数

KAFKA_LOCATION # Kafkaを動作させるマシンの場所 e.g., 'localhost:9092'
# 以下はKafkaのトピックに関する設定です．
# ScrapyとFronteraの間で一致していればなんでも良いですが，デフォルトの名前を少し変更するくらいが妥当に思います．
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
HBASE_THRIFT_HOST = 'localhost' # HBaseが動作するマシンの場所
HBASE_THRIFT_PORT = 9090 # HBaseのThriftクライアントが動作するポート番号 デフォルト9090です
HBASE_METADATA_TABLE = 'metadata' # Fronteraによって作成されるテーブル名．作成されていない場合はFronteraで自動作成します
HBASE_QUEUE_TABLE = 'queue' # Fronteraによって作成されるテーブル名．作成されていない場合はFronteraで自動作成します
```

### Kafka, HBaseの設定
Kafkaを導入，トピック（上の `SPIDER_LOG_TOPIC, SPIDER_FEED_TOPIC, SCORING_LOG_TOPIC` と一致させる）を作成してください．

以下にコマンド例を示します．詳しくは[kafkaのドキュメント](https://kafka.apache.org/documentation/#quickstart)を参照して下さい．
```
$ /path/to/kafka/bin/kafka-topics.sh --create --topic frontier-done --replication-factor 1 --partitions 1 --zookeeper localhost:2181
$ /path/to/kafka/bin/kafka-topics.sh --create --topic frontier-score --replication-factor 1 --partitions 1 --zookeeper localhost:2181
$ /path/to/kafka/bin/kafka-topics.sh --create --topic frontier-todo --replication-factor 1 --partitions 2 --zookeeper localhost:2181
```

また，HBaseを導入し，`crawler` というnamespaceを作成してください．

以下にコマンド例を示します．詳しくは[HBaseのドキュメント](https://hbase.apache.org/book.html#_namespace)を参照して下さい．
```
$ hbase shell
> create_namespace 'crawler'
```

## 動かし方
### Frontera
Kafka + zookeeperが動いていることが前提です．

ターミナルを2つ立ち上げ，fronteraの各ワーカを起動します．`run_*.sh` 内でfronteraのワーカが終了するたびに再起動するようにしています．

```
$ cd /path/to/project/root
$ bash scripts/run_db.sh
```
```
$ cd /path/to/project/root
$ bash scripts/run_strategy.sh
```

終了時には，以下のようにfronteraを終了させます．fronteraのループを止めるスクリプトを叩くようにしています．
```
$ cd /path/to/project/root
$ bash scripts/kill_frontera_loop.sh
```

### Scrapy
fronteraの各ワーカが起動していることが前提です．

#### 初回時のセットアップ
プロジェクトルートに以下のように `partition_id.txt` を作成し， `scripts/init.sh` を実行してください．
このときの数字がFronteraが管理するScrapyのIDになります．
この例ではScrapyのIDは0になります．

```
$ cd /path/to/project/root
$ echo 0 > partition_id.txt
$ bash scripts/init.sh
```

#### Scrapyの起動手順
Scrapyの数だけターミナルを立ち上げ，Scrapyを起動します．fronteraと同様，シェルスクリプト内でScrapyが終了するたびに再起動するようにしています．
```
$ cd /path/to/project/root
$ bash scripts/loop_scrapy.sh
```

Scrapyのログは `scrapy_log/scrapy.log` に吐き出されます．pythonのloggingモジュールによってローテーションがかかることがあるので，監視する場合は `tail -F` を使うと良いと思います．

```
$ tail -F ~/workspace/frontera7/japanese_company_spider[0,1]/scrapy_log/scrapy.log
```
