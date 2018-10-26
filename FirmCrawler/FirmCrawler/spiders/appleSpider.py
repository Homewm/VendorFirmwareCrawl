# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.20"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class AppleSpider(Spider):
    name = "apple"
    start_urls = [
        "http://www.shuaji.com/apple/gujian/"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    headurl = "http://www.shuaji.com/"


    def parse(self, response):
        ul_list = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/ul')
        for ul in ul_list:
            li_list = ul.xpath('./li')
            # print len(li_list)
            for li in li_list:
                href = li.xpath('./a/@href').extract().pop()
                url = urlparse.urljoin(self.headurl, href)
                request = scrapy.Request(url, callback=self.parse_list)
                yield request

    def parse_list(self, response):
        div_list = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div[@class="subox"]')
        for div in div_list:
            li_list = div.xpath('./ul/li')
            # print len(li_list)
            for li in li_list:
                href = li.xpath('./a/@href').extract().pop()
                url = urlparse.urljoin(self.headurl, href)
                request = scrapy.Request(url, callback=self.parse_page)
                yield request

    def parse_page(self, response):
        filename = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div[1]/div[2]/h1/text()').extract().pop()
        # print filename
        version = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div[1]/div[2]/font/a[1]/text()').extract().pop()
        productVersion = version.split("固件")[0]
        # print productVersion
        productModel = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div[1]/div[2]/font/a[2]/text()').extract().pop()
        # print productModel
        description = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div[3]')
        # print description
        desc = description.xpath('string(.)').extract().pop()
        # print desc

        absurl = response.xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div[1]/div[2]/a/@href').extract().pop()
        # print absurl

        if "iPhone".lower() in productModel.lower():
            productClass = "phone"
        elif "iPad".lower() in productModel.lower():
            productClass = "pad"
        elif "Touch".lower() in productModel.lower():
            productClass = "smart watch"
        else:
            productClass = ""
        # print productClass

        item = MI.FirmcrawlerItem()
        item["firmwareName"] = filename
        item["productVersion"] = productVersion
        item["productModel"] = productModel
        item["productClass"] = productClass
        item["publishTime"] = ""
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = desc
        item["manufacturer"] = "apple"

        yield item
        print "firmwarename:", item["firmwareName"]
