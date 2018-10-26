# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.21"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class MicropythonSpider(Spider):
    name = "micropython"
    start_urls = ["http://www.micropython.org/download"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    def parse(self, response):
        ul_list = response.xpath("/html/body/div[2]/div/div/ul")
        # print ul_list
        for ul in ul_list:
            li_list = ul.xpath("./li")
            for li in li_list:
                version = li.xpath("./a/text()").extract().pop()
                # print version
                absurl = li.xpath("./a/@href").extract().pop()
                # print absurl
                filename = absurl.split("/")[-1]
                # print filename

                item = MI.FirmcrawlerItem()
                item["firmwareName"] = filename
                item["productVersion"] = version
                item["productModel"] = ""
                item["productClass"] = ""
                item["publishTime"] = ""
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absurl
                item["description"] = ""
                item["manufacturer"] = "micropython"

                yield item
                print "firmwarename:", item["firmwareName"]
