# -*- coding: utf-8 -*-
import scrapy
import simplejson as json
import os
import pprint as pp
from scrapy.http import Request
from alwadifa.items import AlwadifaItem


class AppSpider(scrapy.Spider):
    name = 'app'
    start_urls = ['http://alwadifa-club.com/']
    data = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.json')))


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        urls = response.xpath(self.data[str(response.url)]['offres']).extract()
        for url in urls:
            req = Request(response.urljoin(url), callback=self.parse_links, dont_filter=True)
            req.meta["detail"] = self.data[str(response.url)]['detail']
            yield req

    def parse_links(self, response):
        detail = response.meta['detail']
        item = AlwadifaItem()
        item['publication'] = response.xpath(detail["publication"]).extract_first()
        item['titre'] = response.xpath(detail["titre"]).extract_first()
        item['image'] = response.xpath(detail["image"]).extract_first()
        item['body'] = response.xpath(detail["body"]).extract_first()
        yield item