# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *

MAX_NEXT_REQUESTS = 512
DELAY_ON_EMPTY = 3.0

#--------------------------------------------------------
# Crawl frontier backend
#--------------------------------------------------------
BACKEND = 'frontera.contrib.backends.remote.messagebus.MessageBusBackend'

MESSAGE_BUS = 'frontera.contrib.messagebus.kafkabus.MessageBus'

#--------------------------------------------------------
# Logging
#--------------------------------------------------------
LOGGING_ENABLED = True
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = False
LOGGING_BACKEND_ENABLED = False
LOGGING_DEBUGGING_ENABLED = False
