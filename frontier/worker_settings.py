# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *

MAX_NEXT_REQUESTS = 512
NEW_BATCH_DELAY = 5.0
CRAWLING_STRATEGY = 'frontier.myCrawlingStrategy.CrawlingStrategy'

#--------------------------------------------------------
# Url storage
#--------------------------------------------------------

BACKEND = 'frontera.contrib.backends.hbase.HBaseBackend'

HBASE_DROP_ALL_TABLES = True
HBASE_THRIFT_PORT = 9090
HBASE_THRIFT_HOST = 'localhost'
HBASE_METADATA_TABLE = 'metadata'
HBASE_QUEUE_TABLE = 'queue-for'

MESSAGE_BUS = 'frontera.contrib.messagebus.kafkabus.MessageBus'

#--------------------------------------------------------
# Logging
#--------------------------------------------------------
LOGGING_CONFIG='logging.conf'
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = True
LOGGING_BACKEND_ENABLED = True
LOGGING_DEBUGGING_ENABLED = False

