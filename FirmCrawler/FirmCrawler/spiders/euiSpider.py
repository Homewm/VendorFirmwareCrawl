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


class euiSpider(Spider):
    name = "eui"
    start_urls = ["http://ui.letv.com/website/downloads/"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3
    headurl = "http://ui.letv.com/"


    def parse(self, response):
        for page in range(1,5):
            url = "http://ui.letv.com/website/downloads/list_" + str(page) + ".html"
            request = scrapy.Request(url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        dl_list = response.xpath("/html/body/div[3]/div[3]/div[1]/dl")
        for dl in dl_list:
            href = dl.xpath("./dt/a/@href").extract().pop()
            url = urlparse.urljoin(self.headurl, href)
            request = scrapy.Request(url, callback=self.parse_list)
            yield  request

    def parse_list(self, response):
        productModel = response.xpath(".//*[@id='editionlist']/div/p/text()").extract().pop()
        # print productModel
        div_list = response.xpath(".//*[@id='editionlist']/div/div[2]/div[position()>3]")

        version = ""
        publishTime = ""
        absurl = ""
        filename = ""
        print len(div_list)
        for i in range(0, len(div_list)):
            if i % 3 == 0 :
                version = div_list[i].xpath("./text()").extract().pop()
                # print version
            if i % 3 == 1:
                publishTime = div_list[i].xpath("./text()").extract().pop()
                # print publishTime
            if i % 3 == 2:
                absurl  = div_list[i].xpath("./a/@href").extract().pop()
                # print absurl

                filename = absurl.split("/")[-1]
            # print version
            # print publishTime
            # print absurl
            # print filename


            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["productVersion"] = version
            item["productModel"] = productModel
            item["productClass"] = "TV"
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = ""
            item["manufacturer"] = "eui"

            yield item
            print "firmwarename:", item["firmwareName"]
