import pymongo
from scrapy.http.response.html import HtmlResponse
import os
import time
import sys
from crawler.save2file import save2file

class MongoPipeline(object):
    collection_name = 'scrapy_items'
    SEPARATOR = "/"
    
    #def __init__(self, mongo_uri, mongo_db):
    #    self.mongo_uri = mongo_uri
    #    self.mongo_db = mongo_db

    @classmethod
    #def from_crawler(cls, crawler):
    #    return cls(
    #        mongo_uri=crawler.settings.get('MONGO_URI'),
    #        mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #    )

    #def open_spider(self, spider):
    #    self.client = pymongo.MongoClient(self.mongo_uri)
    #    self.db = self.client[self.mongo_db]

    #def close_spider(self, spider):
    #    self.client.close()

    def process_item(self, item, spider):
        #print("pipeline: pid = " + str(os.getpid()))

        # ここからresponceのパース処理を書いていく
        directory = os.environ['HOME']
        save2file(scrapy_response = item['response'], outputdir = directory)

        #item['response'] = item['response'].selector.xpath("//h1").extract()
        #print("item['title'] = " + str(item['title']))
        #print("Please activate save2file and deactivate splash")
        #ここまで

        # self.db[self.collection_name].insert(dict(item))
        return item
