# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.22"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import time


class sundraySpider(Spider):
    name = "sundray"
    timeout = 20
    trytimes = 3
    #only 胖AP升级包 is what we need
    start_urls = ["http://www.sundray.com.cn/data/32.html"]
    # must be lower character
    typefilter = ["txt", "pdf", "apk"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,7+1): #3+1
            url = "http://www.sundray.com.cn/data/32_page_%s.html" %i
            if i == 1:
                url = "http://www.sundray.com.cn/data/32.html"
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "sundray"
            yield request

    def parse_list(self, response):
        tables = response.xpath('//div[@id="ndown"]/dl')
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        for t in tables:
            url1 = t.xpath('./dd[6]/a/@href').extract()[0]
            publishtime = t.xpath('./dd[5]/text()').extract()[0]
            desc = t.xpath('./dd[2]//text()').extract()[0].strip()
            filename = url1.split("/")[-1]
            item["productVersion"] = ""
            item["publishTime"] = publishtime
            item["productClass"] = "Router"
            item["productModel"] = ""
            item["description"] = desc
            item["url"] = url1
            item["firmwareName"] = filename
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            yield item
            print "firmwarename:", item["firmwareName"]