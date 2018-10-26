# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.03.14"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class mercurySpider(Spider):
    name = "mercury"
    timeout = 20
    trytimes = 3
    start_urls = ["http://service.mercurycom.com.cn/download-list.html"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,25): #20+1
            url = "http://service.mercurycom.com.cn/download-list.html?p=%s" %i
            # print "url:",url
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "mercury"
            yield request

    def parse_list(self, response):
        tables = response.xpath('//div[@class="downpart"]/table/tbody//a/@href').extract()
        for t in tables:
            url = urlparse.urljoin(response.url,t)
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "mercury"
            yield request
    def parse_page(self,response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        tables = response.xpath('//div[@class="download-detail"]/table/tbody/tr[4]/td[2]/a/@href').extract().pop()
        absurl = urlparse.urljoin(response.url,tables.replace(' ','%20'))
        filename = tables.split('/')[-1]
        softname = response.xpath('//div[@class="download-detail"]/table/tbody/tr[1]/td[2]/p/text()').extract().pop().strip()
        desc = response.xpath('//div[@class="download-detail"]/table/tbody/tr[5]/td[2]//text()').extract()
        publishtime = response.xpath('//div[@class="download-detail"]/table/tbody/tr[3]/td[2]/p/text()').extract().pop()
        try:
            array = time.strptime(publishtime, u"%Y/%m/%d")
            item["publishTime"] = time.strftime("%Y-%m-%d", array)
        except Exception, e:
            print e
        model = softname.split(' ')[0]
        version = softname.split(' ')[-1].split('_')[0]
        item["productVersion"] = version
        item["productClass"] = "" #more class
        item["productModel"] = model
        item["description"] = str().join(desc).strip()
        item["url"] = absurl
        item["firmwareName"] = filename
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        yield item
        print "firmwarename:",item["firmwareName"]
        return



