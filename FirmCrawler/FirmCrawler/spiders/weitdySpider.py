# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.10"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import re


class WeitdySpider(Spider):
    name = "weitdy"
    allowed_domain = ["weitdy.com"]
    start_urls = ["http://www.weitdy.com/list/?80_1.html"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3
    headurl = "http://www.weitdy.com"


    def parse(self, response):

        tr_list = response.xpath('//html/body/div[9]/div[2]/div[2]/table/tr[position()>1]')
        # print len(tr_list)
        for tr in tr_list:
            href = tr.xpath('./td[2]/a/@href').extract().pop()
            url = urlparse.urljoin(self.headurl, href)

            request = scrapy.Request(url, callback=self.parse_page)
            yield request


    def parse_page(self, response):
        filename = response.xpath('//html/body/div[9]/div[2]/div[1]/text()').extract().pop()
        publish_Time = response.xpath('//html/body/div[9]/div[2]/div[2]/ul/li[5]/text()').extract().pop()
        publishTime = publish_Time.split(" ")[0]
        # print publishTime
        product_Model = response.xpath('//html/body/div[9]/div[2]/div[4]/p[2]/strong/span/text()').extract()
        if product_Model:
            productModel = product_Model.pop()
        else:
            productModel = ""

        desc_info = response.xpath('//html/body/div[9]/div[2]/div[4]/p[4]/span/text()').extract()
        # print desc_info
        desc = ""
        if desc_info:
            for d in desc_info:
                desc = desc + d.strip()
        elif response.xpath('//html/body/div[9]/div[2]/div[4]/p[3]/span/text()').extract():
            for d in desc_info:
                desc = desc + d.strip()
        else:
            desc = ""

        href = response.xpath('//html/body/div[9]/div[2]/div[5]/a/@href').extract().pop()
        absurl = urlparse.urljoin(self.headurl, href)
        print absurl


        item = MI.FirmcrawlerItem()
        item["firmwareName"] = filename
        item["publishTime"] = publishTime
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = desc
        item["productClass"] = ""
        item["productVersion"] = ""
        item["productModel"] = productModel
        item["manufacturer"] = "weitdy"

        yield item
        print "firmwarename:", item["firmwareName"]
