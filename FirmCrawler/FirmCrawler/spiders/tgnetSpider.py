# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.04.17"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class uttSpider(Spider):
    name = "tgnet"
    timeout = 20
    allowed_domains = ["tg-net.cn"]
    trytimes = 3
    start_urls = ["http://www.tg-net.cn/download.html"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,12+1): #12+1
            url = "http://www.tg-net.cn/download_106_%s.html" %i
            # print "url:",url
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "TG-NET"
            yield request

    def parse_list(self, response):
        tables = response.xpath('//div[@class="list"]/dl//@href').extract()
        for t in tables:
            url = urlparse.urljoin(response.url,t)
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "tg-net"
            yield request
    def parse_page(self,response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        tables = response.xpath('//div[@class="list"]/table/tr[4]//a/@href').extract()
        absurl = urlparse.urljoin(response.url,tables[0])
        filename = tables[0].split('/')[-1].replace(".online","")
        softname = response.xpath('//div[@class="list"]/table/tr[1]/td/text()').extract().pop().strip()
        version = re.search('[V,v]?\d\.\d\.\d\.*\d*',softname)
        if version:
            version = version.group()
        else:
            version = ""
        if version:
            model = softname.split(" ")[-1].split(version)[0]
        else:
            model = softname
        model = unicode.encode(model,encoding='utf8').replace("-","").replace("_","")
        item["productVersion"] = version
        item["publishTime"] = ""
        item["productClass"] = ""
        item["productModel"] = model.replace("-","").replace("_","")
        item["description"] = ""
        item["url"] = absurl
        item["firmwareName"] = filename
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        yield item
        print "firmwarename:",item["firmwareName"]



