# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.04.16"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

class lblinkSpider(Spider):
    name = "lblink"
    timeout = 8
    trytimes = 3
    start_urls = ["http://www.b-link.net.cn/download.php?CateId=11"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        for i in xrange(1,3+1):
            url = "http://www.b-link.net.cn/download.php?CateId=11&page=%s" %i
            request = scrapy.Request(url, callback=self.parse_list)
            yield request

    def parse_list(self, response):
        tables = response.xpath('//ul[@id="lib_download_list"]/li//a/@href').extract()
        for t in tables:
            url = urlparse.urljoin(response.url,t)
            request = scrapy.Request(url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        urls = response.xpath('//div[@class="download_rig fr"]/a/@href').extract()[0]
        absurl = urlparse.urljoin(response.url, urls)
        info = response.xpath('//div[@class="download_rig fr"]//text()').extract()
        info = str().join(info).strip()
        info = unicode.encode(info,encoding='utf8')
        modelt = info.split(r"路由器型号：")[-1]
        if "固件版本" in modelt:
            model = modelt.split(r"固件版本：")[0].strip()
            version = modelt.split(r"固件版本：")[-1].split(r"固件大小：")[0].strip()
        else:
            model = modelt.split(r"固件大小：")[0].strip()
            version = ""
        publishtime = modelt.split(r"上传日期：")[-1].split(r"软件简介：")[0].strip()
        desc = modelt.split(r"软件简介：")[-1].split("。")[0].strip()

        item = MI.FirmcrawlerItem()
        item["url"] = absurl
        try:
            res = urllib2.urlopen(urllib2.Request(
                item["url"], None), timeout=lblinkSpider.timeout)
            contentType = res.headers["content-type"]
            filename = contentType.split('\"')[1]
            item["firmwareName"] = filename
        except Exception, e:
            print "no firmware name"
            print e


        item["productVersion"] = version.split("\r\n")[0]
        item["publishTime"] = publishtime.split("\r\n")[0]
        item["productClass"] = "Router"
        item["productModel"] = model.split(" ")[0]
        item["description"] = desc
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["manufacturer"] = "lblink"
        yield item
        print "firmwarename:", item["firmwareName"]


