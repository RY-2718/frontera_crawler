from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from crawler.items import TestItem
import urllib
import os
import re
import logging
from crawler.blacklist import blacklist
import chardet
import cgi
from six.moves.urllib.parse import urlparse

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)
ignore_logger = logging.getLogger("ignore_logger")

#foreign_encodings = ["Big5", "GB2312", "GB18030", "EUC-TW", "HZ-GB-2312", "ISO-2022-CN",
#                  "EUC-JP", "SHIFT_JIS", "ISO-2022-JP",
#                  "EUC-KR", "ISO-2022-KR",
#                  "KOI8-R", "MacCyrillic", "IBM855", "IBM866", "ISO-8859-5", "windows-1251",
#                  "ISO-8859-2", "windows-1250",
#                  "ISO-8859-5", "windows-1251",
#                  "ISO-8859-1", "windows-1252",
#                  "ISO-8859-7", "windows-1253",
#                  "ISO-8859-8", "windows-1255",
#                  "TIS-620",
#                  ]

chinese_encodings = ["Big5", "GB2312", "GB18030", "EUC-TW", "HZ-GB-2312", "ISO-2022-CN"]

class GeneralSpider(Spider):
    # 最初の方はScrapyそのものを動かすための記述
    name = 'crawler'

    deny_domain_list = []
    deny_list = []

    blist = blacklist(os.path.dirname(os.path.abspath(__file__)) + '/../../txt/blacklist.txt')
    deny_list.extend(blist)

    def __init__(self, *args, **kwargs):
        super(GeneralSpider, self).__init__(*args, **kwargs)
        self.le = LinkExtractor(
            deny=self.deny_list,
            deny_domains=self.deny_domain_list,
        )

    def parse(self, response):
        if (not isinstance(response, HtmlResponse)) or response.status != 200:
            return

        true_encoding = None

        if response.encoding is 'ascii':
            for content_type in response.headers.getlist('Content-Type'):
              _, params = cgi.parse_header(content_type.decode('utf-8'))
              if params.get('charset') is not None:
                true_encoding = params.get('charset')
                break

            # detect language and encoding
            if true_encoding is None:
                chardet_result = chardet.detect(response.body)
                true_encoding = chardet_result['encoding']
                if chardet_result['language'] is 'Chinese':
                    title = response.xpath('/html/head/title/text()').extract()
                    if len(title) > 0:
                        title = title[0].encode('utf-8').decode(true_encoding)
                        ignore_logger.debug("%s %s" % (response.url, title))
                        print("%s is a chinese url: %s" % (response.url, title))
                    return
        else:
            true_encoding = response.encoding

        # asciiやろ！って場合utf-8に変えて事故を減らす
        response_encoding = response.encoding
        if response_encoding is 'ascii':
            response_encoding = 'utf-8'

        # 文字コードから言語を判定してスキップするか決める
        if true_encoding in chinese_encodings:
            title = response.xpath('/html/head/title/text()').extract()
            title = title[0].encode(response_encoding).decode(true_encoding)
            ignore_logger.debug("%s %s chinese charset" % (response.url, title))
            print("chinese charset: %s %s" % (response.url, title))
            return

        # 返ってきたHTMLからURLを抽出して次の要求を出す
        for link in self.le.extract_links(response):

            r = Request(url=link.url,
                    callback=self.parse,
                )
            r.meta.update(link_text=link.text)
            yield r

        # 返ってきたHTMLのパース部分
        # ここではHTMLをまるごと返すのみで，pipeline.pyで細かい処理を行っていく．
        #print("spider: pid = " + str(os.getpid()))
        item = TestItem()
        url = response.url
        #title = response.xpath('/html/head/title/text()').extract()
        res = response
        item['url'] = url
        item['response'] = res
        yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GeneralSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._set_crawler(crawler)
        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def spider_idle(self):
        self.log("Spider idle signal caught.")
        raise DontCloseSpider
