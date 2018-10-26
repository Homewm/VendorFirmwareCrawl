# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.19"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import string


class KosSpider(Spider):
    name = "kos"
    allowed_domain = ["kos.org.cn"]
    start_urls = [
        "http://upacimg.kos.org.cn/ap.html",
        "http://upacimg.kos.org.cn/index.html"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3


    def parse(self, response):
        url = response.url
        product_class = url.split("/")[-1].split(".")[0]
        if product_class == "index":
            productClass = "AC"
        elif product_class == "ap":
            productClass = "AP"
        else:
            productClass = ""

        tr_list = response.xpath('/html/body/table/tr[position()>1]')
        # print tr_list
        for tr in tr_list:
            href  = tr.xpath('./td[2]/a/@href').extract().pop()
            if href:
                absurl = href
                filename = tr.xpath('./td[2]/a/text()').extract().pop()
                # print filename
                productModel = tr.xpath('./td[3]/text()').extract().pop()
                # print productModel
                filesize = tr.xpath('./td[4]/text()').extract().pop()
                md5 = tr.xpath('./td[5]/text()').extract().pop()
                desc = "filesize:" + str(filename) + ";  " + "md5:" + str(md5)
                publishTime = tr.xpath('./td[6]/text()').extract().pop().split(" ")[0]
                # print productModel
                # print desc
                # print publishTime

                item = MI.FirmcrawlerItem()
                item["firmwareName"] = filename
                item["publishTime"] = publishTime
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absurl
                item["description"] = desc
                item["productClass"] = productClass
                item["productVersion"] = ""
                item["productModel"] = productModel
                item["manufacturer"] = "kos"

                yield item
                print "firmwarename:", item["firmwareName"]
