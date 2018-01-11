from __future__ import absolute_import
from frontera.settings.default_settings import MIDDLEWARES

MAX_NEXT_REQUESTS = 32
DELAY_ON_EMPTY = 3.0

SPIDER_FEED_PARTITIONS = 2 # number of spider processes
SPIDER_LOG_PARTITIONS = 1 # strategy worker instances

MIDDLEWARES.extend([
    'frontera.contrib.middlewares.domain.DomainMiddleware',
    'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
])

QUEUE_HOSTNAME_PARTITIONING = True
HBASE_USE_SNAPPY = False
KAFKA_LOCATION = 'localhost:9092' # your Kafka broker host:port
SPIDER_LOG_DBW_GROUP = 'dbw-spider-log'
SPIDER_LOG_SW_GROUP = 'sw-spider-log'
SCORING_LOG_DBW_GROUP = 'dbw-scoring-log'
SPIDER_FEED_GROUP = 'fetchers-spider-feed'
SPIDER_LOG_TOPIC = 'frontier-done'
SPIDER_FEED_TOPIC = 'frontier-todo'
SCORING_LOG_TOPIC = 'frontier-score'
URL_FINGERPRINT_FUNCTION='frontera.utils.fingerprint.hostname_local_fingerprint'
