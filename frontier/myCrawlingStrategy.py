# -*- coding: utf-8 -*-
from __future__ import absolute_import
from six.moves.urllib.parse import urlparse
from frontera.core.components import States
from frontera.worker.strategies import BaseCrawlingStrategy
import random

class CrawlingStrategy(BaseCrawlingStrategy):

    def add_seeds(self, seeds):
        for seed in seeds:
            if seed.meta[b'state'] is States.NOT_CRAWLED:
                seed.meta[b'state'] = States.QUEUED
                self.schedule(seed)
            elif seed.meta.get(b'scrapy_meta').get(b'rescheduled') or seed.meta.get(b'scrapy_meta').get(b'dupricated'):
                seed.meta[b'state'] = States.QUEUED
                self.schedule(seed)

    def page_crawled(self, response):
        response.meta[b'state'] = States.CRAWLED

    def links_extracted(self, request, links):
        for link in links:
            if link.meta[b'state'] is States.NOT_CRAWLED:
                link.meta[b'state'] = States.QUEUED
                self.schedule(link, self.get_score(link.url))

    def page_error(self, request, error):
        request.meta[b'state'] = States.ERROR
        self.schedule(request, score=0.0, dont_queue=True)

    def schedule(self, request, score=1.0, dont_queue=False):
        """
        Schedule document for crawling with specified score.
        :param request: A :class:`Request <frontera.core.models.Request>` object.
        :param score: float from 0.0 to 1.0
        :param dont_queue: bool, True - if no need to schedule, only update the score
        """
        dupricate_correction = 1.0
        if request.meta.get(b'scrapy_meta').get(b'dupricated'):
            print("dupricated: " + request.url)
            score = self.get_score(request.url)
            dupricate_correction = random.uniform(0.85, 0.99)
            print("score = " + str(score * dupricate_correction))
        if request.meta.get(b'scrapy_meta').get(b'rescheduled'):
            score = self.get_score(request.url)
            dont_queue=False
        self._mb_stream.send(request, score * dupricate_correction, dont_queue)

    def get_score(self, url):
        url_parts = urlparse(url)
        path_parts = url_parts.path.split('/')
        query_parts = url_parts.query.split('&')
        return 1.0 / (max(len(path_parts) + len(query_parts), 1.0) + len(url_parts.path + url_parts.query) * 0.1)
