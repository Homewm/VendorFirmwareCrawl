# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.03.20"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse,urllib,urllib2
import time

class tomaxSpider(Spider):
    name = "tomax"
    timeout = 20
    trytimes = 3
    start_urls = ["http://www.tomaxcom.com/shengjiruanjian/list_30_1.html"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,5+1): #5+1
            url = "http://www.tomaxcom.com/shengjiruanjian/list_30_%s.html" %i
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "tomax"
            yield request

    def parse_list(self, response):
        tables = response.xpath('//table[@id="con_two_1"]/tr[position()>1]')
        for t in tables:
            urls = t.xpath('./td[1]/a/@href').extract()
            absurl = urlparse.urljoin(response.url,urls[0])
            request = scrapy.Request(absurl, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "tomax"
            yield request
    def parse_page(self,response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        urls = response.xpath('//div[@class="xzbox"]/table/tr[5]//a/@href').extract().pop()
        absurl = urlparse.urljoin(response.url,urls)
        filename = absurl.split('/')[-1]
        softname = response.xpath('//div[@class="xzbox"]/table/tr[1]/td[2]//text()').extract().pop().strip()
        desc = response.xpath('//div[@class="xzbox"]/table/tr[6]/td[2]//text()').extract()
        desc = unicode.encode(str().join(desc),encoding='utf-8').replace("\n","").replace("\t","").replace("\r","").strip()
        publishtime = response.xpath('//div[@class="xzbox"]/table/tr[4]/td[2]//text()').extract().pop().strip().replace("/","-")
        version = re.search("[V,v]\d\.\d\.?\d?", filename)
        if version:
            version = version.group()
            model = filename.split(version)[0]
        else:
            version = ""
            model = ""

        item["productVersion"] = version
        item["publishTime"] = publishtime
        item["productClass"] = ""
        item["productModel"] = model
        item["description"] = str().join(desc).strip()
        item["url"] = absurl
        item["firmwareName"] = filename
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        yield item
        print "firmwarename:",item["firmwareName"]
        return
    #






