# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.21"

'''代码编写后正常使用，涉及点击，但是这个点击比较简单，在页面源码之中够造了链接。'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class OnkyoSpider(Spider):
    name = "onkyo"
    start_urls = ["http://www.cn.onkyo.com/2018newsite/Support/Firmware.html"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    def parse(self, response):
        for p in range(1,4):
            url = "http://www.cn.onkyo.com/2018newsite/Support/Firmware.html?page=" + str(p)
            request = scrapy.Request(url,callback=self.parse_page)
            yield  request

    def parse_page(self, response):
        li_list = response.xpath('//html/body/div[3]/div/div[2]/ul/li')
        for li in li_list:
            did_value = li.xpath('./@did').extract().pop()
            absurl = "http://www.cn.onkyo.com/2018newsite/Download/" + str(did_value) + ".html"
            # print absurl
            file_name = li.xpath('./a/text()').extract().pop()
            filename = file_name.split("固件更新")[0]
            publishTime = file_name.split("固件更新")[-1]
            # print filename
            # print publishTime

            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["productVersion"] = ""
            item["productModel"] = ""
            item["productClass"] = ""
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = ""
            item["manufacturer"] = "onkyo"

            yield item
            print "firmwarename:", item["firmwareName"]
