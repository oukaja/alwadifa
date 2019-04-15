# -*- coding: utf-8 -*-
import scrapy
import simplejson as json
import os


class AppSpider(scrapy.Spider):
    name = 'app'
    start_urls = []
    data = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.json')))

    def parse(self, response):
        print(self.data)
        pass
