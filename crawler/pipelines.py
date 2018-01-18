from crawler.save2file import save2file

class S3Pipeline(object):
    @classmethod
    def process_item(self, item, spider):
        save2file(scrapy_response = item['response'])

        return item
