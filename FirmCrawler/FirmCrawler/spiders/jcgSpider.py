# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.11"

#’‚ «◊¢ Õ
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class jcgSpider(Spider):
    name = "jcg"
    timeout = 20
    trytimes = 3
    start_urls = ["http://www.jcgcn.com/list_42/"]
    # must be lower character
    typefilter = ["txt", "pdf", "apk"]
    allsuffix = Set()

    def parse(self, response):
        for i in xrange(1,3+1): #10+1
            url = "http://www.jcgcn.com/list-42-22-%s/" % i
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "jcg"
            yield request

    def parse_list(self, response):
        lis = response.xpath('//div[@class="technical_support_box"]/ul/li')
        # print len(lis)
        info_urls = lis.xpath('./a/@href').extract()
        for url in info_urls:
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = response.meta["prototype"]
            yield request

    def parse_page(self, response):
        prototype = response.meta['prototype']
        item = MI.FirmcrawlerItem(prototype)
        filename = response.xpath('//div[@class="technical_support_box_z"]/div/div/text()').extract()
        if filename:
            filename = filename[0]
        else:
            filename = ""

        publishTime = response.xpath('//div[@class="technical_support_box_z"]/div/ul/li[2]/text()').extract()[0]
        publishTime = publishTime.strip().split(" ")[0]

        absurl = response.xpath('//div[@class="technical_support_box_z_info_box"]/div[5]/ul/li/a/@href').extract()
        if absurl:
            absurl = absurl[0]
            # print absurl
        else:
            absurl = ""

        desc_li = response.xpath('//div[@class="technical_support_box_z_info_box"]/div[3]/ul/li')
        desc = []
        for desc_info in desc_li:
            desc_ = desc_info.xpath('./font/text()').extract()
            if desc_:
                description = desc_[0]
                # print description
                desc.append(description)
            else:
                description = ""
        if desc:
            desc = " ".join(desc)
        else:
            desc = ""

        item["productVersion"] = ""
        item["publishTime"] = publishTime
        item["productClass"] = ""
        item["productModel"] = ""
        item["description"] = desc
        item["url"] = absurl
        item["firmwareName"] = filename
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["manufacturer"] = "jcg"
        yield item
        print "firmwarename:", item["firmwareName"]




