# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.03.16"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class fastSpider(Spider):
    name = "fast"
    timeout = 20
    trytimes = 3
    start_urls = ["http://service.fastcom.com.cn/download-list.html"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,18+1):
            url = "http://service.fastcom.com.cn/download-list.html?classTip=software&p=%s&o=1&ajax=True&paging=False" %i
            # print "url:",url
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "fast"
            yield request

    def parse_list(self, response):
        tables = response.xpath('//div[@class="container table-container"]//a/@href').extract()
        for t in tables:
            url = urlparse.urljoin(response.url,t)
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "fast"
            yield request
    def parse_page(self,response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        tables = response.xpath('//div[@class="table-wrap"]/table/tbody/tr[4]/td[2]/a/@href').extract().pop()
        absurl = urlparse.urljoin(response.url,tables.replace(' ','%20'))
        filename = tables.split('/')[-1]
        softname = response.xpath('//div[@class="table-wrap"]/table/tbody/tr[1]/td[2]//text()').extract().pop().strip()
        desc = response.xpath('//div[@class="table-wrap"]/table/tbody/tr[5]/td[2]//text()').extract()
        publishtime = response.xpath('//div[@class="table-wrap"]/table/tbody/tr[3]/td[2]//text()').extract().pop()
        model = softname.split(' ')[0]
        version = softname.split(' ')[-1].split('_')[0]
        item["productVersion"] = version
        item["publishTime"] = publishtime.strip()
        item["productClass"] = ""
        item["productModel"] = model
        item["description"] = str().join(desc).strip()
        item["url"] = absurl
        item["firmwareName"] = filename
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        yield item
        print "firmwarename:",item["firmwareName"]
        return



