# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.10"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time


class hiwifiSpider(Spider):
    name = "hiwifi"
    timeout = 20
    trytimes = 3
    start_urls = ["https://app.hiwifi.com/dstore.php?m=download&a=info"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "hiwifi"
        yield request

    def parse_page(self, response):
        prototype = response.meta['prototype']
        rows = response.xpath('//div[@class="download-main"]/ul/li/table/tr/td[position()>1]')
        for r in rows:
            url = r.xpath('./a/@href').extract()
            if len(url):
                url = url.pop()
                print "url:",url
                version = unicode.encode(r.xpath('./p[2]/text()').extract().pop(),encoding='utf-8').split('：')[1].split('s')[0]
                publishtime = r.xpath('./p[1]/text()').extract().pop().split(':')[-1].split(')')[0]
                item = MI.FirmcrawlerItem(prototype)
                item["firmwareName"] = url.split('/')[-1]
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = url
                item["publishTime"] = publishtime
                item["description"] = ""
                item["productVersion"] = version
                item["productModel"] = item["firmwareName"].split('-')[0]
                item["productClass"] = "Router"  # waiting for doing it
                yield item
                print "firmwareName:", item["firmwareName"]
        return


