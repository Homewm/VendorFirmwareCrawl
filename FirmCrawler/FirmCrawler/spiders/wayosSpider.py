#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2018.09.25"


'''网站结构发生改变,代码重写完全后正常使用'''


from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import re


class WayosSpider(Spider):
    name = "wayos"
    allowed_domain = ["wayos.com"]
    start_urls = [
        "http://www.wayos.com/download/luyougujian.html"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3


    def parse(self, response):
        for page in xrange(1,5):
            url_router = "http://www.wayos.com/download/luyougujian/" + str(page) + ".html"
            request = scrapy.Request(url_router, callback=self.parse_list)

            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "Wayos"
            yield request

        for page in xrange(1, 3):
            url_app = "http://www.wayos.com/download/APgujian/" + str(page) + ".html"
            request = scrapy.Request(url_app, callback=self.parse_list)

            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "Wayos"
            yield request


    def parse_list(self, response):
        page_url = response.url

        li_list = response.xpath('//div[@class="download"]/div[1]/li')
        for li in li_list:
            filename = li.xpath('./a/text()').extract().pop()
            absurl = li.xpath('./a/@href').extract().pop()
            publishTime = li.xpath('./span/text()').extract().pop()
            # print publishTime

            productVersion = filename.split("-")[-1].split("固件")[0]
            # print version

            product_class = page_url.split("/")[-2]
            # print product_class
            if "luyou" in product_class:
                productClass = "router"
            elif "APgujian" in product_class:
                productClass = "app"
            else:
                productClass = ""
            # print productClass

            productModel = filename.rsplit("-", 1)[0]
            # print productModel

            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = ""
            item["productClass"] = productClass
            item["productVersion"] = productVersion
            item["productModel"] = productModel
            item["manufacturer"] = "wayos"

            yield item
            print "firmwarename:", item["firmwareName"]







