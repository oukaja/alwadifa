# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
import simplejson as json
import os
import pprint as pp
from scrapy.http import Request
from alwadifa.items import AlwadifaItem
from bidi.algorithm import get_display
import arabic_reshaper


class AppSpider(scrapy.Spider):
    name = 'app'
    start_urls = ['http://alwadifa-club.com/']
    data = json.load(
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.json')))

  
    @staticmethod
    def dateFormat(dateAr):
        months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'ماي', 'يونيو', 'يوليوز', 'غشت', 'شتنبر', 'أكتوبر', 'نونبر', 'دجنبر']
        i = 0
        dateAr = str(dateAr)
        onlyDate = dateAr.split()
        d = onlyDate[0]
        m = onlyDate[1]
        y = onlyDate[2]
        for item in months:
            i = i + 1
            if item in m:
                break
        return  d + '-' + str(i) + '-' + y

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath(self.data[str(response.url)]['offres']).extract()
        for url in urls:
            req = Request(response.urljoin(url),
                          callback=self.parse_links, dont_filter=True)
            req.meta["detail"] = self.data[str(response.url)]['detail']
            req.meta["url"] = str(response.url)
            yield req

    def parse_links(self, response):
        detail = response.meta['detail']
        url = response.meta['url']
        item = AlwadifaItem()
        if url == 'http://alwadifa-club.com/':
            item['link'] = str(response.url)
            item['publication'] = self.dateFormat(str(response.xpath(detail["publication"]).extract_first()))
            item['titre'] = response.xpath(detail["titre"]).extract_first()
            item['body'] = response.xpath(detail["body"]).extract_first()
        yield item
