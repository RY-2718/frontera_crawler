import scrapy

class TestItem(scrapy.Item):
    url = scrapy.Field()
    response = scrapy.Field()
    pass
