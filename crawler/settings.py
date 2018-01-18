# -*- coding: utf-8 -*-

# Scrapy settings for topic project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from scrapy.settings.default_settings import SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

# S3 bucket name
BUCKET_NAME = ''

# frontera settings
SPIDER_MIDDLEWARES.update({
    'frontera.contrib.scrapy.middlewares.seeds.file.FileSeedLoader': 1,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 1000,
    'scrapy.spidermiddleware.depth.DepthMiddleware': None,
    'scrapy.spidermiddleware.offsite.OffsiteMiddleware': None,
    'scrapy.spidermiddleware.referer.RefererMiddleware': None,
    'scrapy.spidermiddleware.urllength.UrlLengthMiddleware': None
})

DOWNLOADER_MIDDLEWARES.update({
    'crawler.middlewares.IPCheckerMiddleware': 1,
    #'crawler.middlewares.DenyBlacklistDomainMiddleware': 2,
    #'crawler.middlewares.ReturnQueryURLMiddleware': 3,
    'crawler.middlewares.DownloadTooMuchAtOnceCheckerMiddleware': 4,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware': 1000,
})

ITEM_PIPELINES = {
    'crawler.pipelines.S3Pipeline': 800,
}

SCHEDULER = 'frontera.contrib.scrapy.schedulers.frontier.FronteraScheduler'

HTTPCACHE_ENABLED = False
REDIRECT_ENABLED = True
DOWNLOAD_TIMEOUT = 30
RETRY_ENABLED = False
#DOWNLOAD_MAXSIZE = 10*1024*1024

# auto throttling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_MAX_DELAY = 3.0
AUTOTHROTTLE_START_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = False

# concurrency
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_DELAY = 0.0

LOG_LEVEL = 'INFO'

REACTOR_THREADPOOL_MAXSIZE = 32
DNS_TIMEOUT = 30
