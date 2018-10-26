# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.03.25"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class VipaSpider(Spider):
    name = "totolink"
    timeout = 20
    trytimes = 3
    start_urls = [
        "http://www.totolink.cn/index.php/Index/dowmload?module=Download&pname2=&submit=%E6%90%9C%E7%B4%A2"
    ]
    # must be lower character
    typefilter = ["txt", "pdf","apk"]
    allsuffix = Set()

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "totolink"
        yield request

    def parse_page(self, response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        tables = response.xpath('//div[@class="sofewear"]/table[1]/tbody/tr')
        for t in tables:
            softname = t.xpath('./td[2]/a/text()').extract().pop().strip()
            if "驱动" not in unicode.encode(softname,encoding='utf-8'):
                url = t.xpath('./td[2]/a/@href').extract()
                absurl = urlparse.urljoin(response.url,url[0]).replace(" ","%20").replace("(","%28").replace(")","%29")
                model = t.xpath('./td[1]/text()').extract().pop().strip()
                publishtime = t.xpath('./td[4]/text()').extract().pop()
                version = re.search("[V,v]?\d\.\d", softname)
                if version:
                    version = version.group()
                else:
                    version = ""
                item["productVersion"] = version
                item["publishTime"] = publishtime
                item["productClass"] = ""
                item["productModel"] = model
                item["description"] = softname
                item["url"] = absurl
                item["firmwareName"] = item["url"].split('/')[-1]
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                yield item
                print "firmwarename:", item["firmwareName"]
            else:
                print "qudong :",softname

