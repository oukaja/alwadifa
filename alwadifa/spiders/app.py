# -*- coding: utf-8 -*-
import scrapy


class AppSpider(scrapy.Spider):
    name = 'app'
    allowed_domains = ['alwadifa']
    start_urls = ['http://alwadifa/']

    def parse(self, response):
        pass
