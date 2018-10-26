# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.03.05"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class draytekSpider(Spider):
    name = "draytek"
    timeout = 20
    trytimes = 3
    start_urls = [
        "http://www.draytek.com.cn/support/DownloadShow.php"
    ]

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_list)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "draytek"
        yield request

    def parse_list(self,response):
        lists = response.selector.xpath('//body/table[1]//table//tr[position()>3]')
        for l in lists:
            url = l.xpath('./td[3]//a/@href').extract()
            absurl = urlparse.urljoin(response.url,url[0])
            request = scrapy.Request(absurl, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "draytek"
            yield request


    def parse_page(self, response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        lists = response.selector.xpath('//body/table[1]/tr[1]/td/div')
        model = lists.xpath('./span/text()').extract().pop().strip().split(":")[-1]
        table = lists.xpath('./table//tr[position()>1]')
        for t in table:
            version = t.xpath('./td[1]//text()').extract().pop()
            publishtime = t.xpath('./td[2]//text()').extract().pop().replace("/","-")
            urls = t.xpath('./td[5]//a/@href').extract()
            absurl = urlparse.urljoin(response.url,urls[0])
            item["productVersion"] = version
            item["publishTime"] = publishtime
            item["productClass"] = ""
            item["productModel"] = model
            item["description"] = ""
            item["url"] = absurl
            item["firmwareName"] = item["url"].split('/')[-1]
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            yield item
            print "firmwarename:", item["firmwareName"]
