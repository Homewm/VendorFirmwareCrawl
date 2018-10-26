# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.17"

from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class uttSpider(Spider):
    name = "utt"
    timeout = 20
    trytimes = 3
    start_urls = ["http://www.utt.com.cn/downloadcenter.php"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,56+1): #56+1
            url = "http://www.utt.com.cn/downloadcenter.php?page=%s&filetypeid=3&productmodelid=0" %i
            # print "url:",url
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "utt"
            yield request

    def parse_list(self, response):
        tables = response.xpath('//div[@class="fw_downresult"]/div/a[1]/@href').extract()
        for t in tables:
            url = urlparse.urljoin(response.url,t)
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "UTT"
            yield request
    def parse_page(self,response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        tables = response.xpath('//div[@class="fwglobalcontent-noborder"]/table/tr[5]/td[2]/a/@href').extract()
        absurl = urlparse.urljoin(response.url,tables[0])
        filename = tables[0].split('/')[-1]
        softname = response.xpath('//div[@class="fwglobalcontent-noborder"]/table/tr[1]/td[2]//text()').extract().pop().strip()
        desc = response.xpath('//div[@class="fwglobalcontent-noborder"]/table/tr[6]/td[2]//text()').extract()
        publishtime = response.xpath('//div[@class="fwglobalcontent-noborder"]/table/tr[4]/td[2]//text()').extract().pop()
        softnameinfo = unicode.encode(softname,encoding="utf8")
        softnameinfo = softnameinfo.split("版本")[0].replace("过渡","")
        model = softnameinfo.rsplit('v',1)[0]
        version = softnameinfo.rsplit('v')[-1].split('-')[0]
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



