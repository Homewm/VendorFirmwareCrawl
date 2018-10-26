# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.21"

'''代码编写后正常使用'''
'''网页固件比较少，就6个'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class AutobotSpider(Spider):
    name = "autobot"
    start_urls = ["http://autobot.im/appdownload.cfm"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    def parse(self, response):
        div_list = response.xpath("/html/body/div[5]/div[8]/div/div")
        for div in div_list:
            absurl = div.xpath("./a/@href").extract().pop()
            filename = absurl.split("/")[-1]

            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["productVersion"] = ""
            item["productModel"] = ""
            item["productClass"] = ""
            item["publishTime"] = ""
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = ""
            item["manufacturer"] = "autobot"

            yield item
            print "firmwarename:", item["firmwareName"]
