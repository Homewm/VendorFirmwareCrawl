# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.08"


'''新探索网站,代码编写后正常使用'''


from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import re


class ComfastSpider(Spider):
    name = "comfast"
    allowed_domain = ["comfast.cn"]
    start_urls = [
        "http://www.comfast.cn/index.php?m=content&c=index&a=lists&catid=31#orientate"
        # "http://www.comfast.cn/index.php?m=content&c=index&a=lists&catid=30#orientate"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    headurl = "http://www.comfast.cn"


    def parse(self, response):
        for i in range(1, 6):
            url = "http://www.comfast.cn/index.php?m=content&c=index&a=lists&catid=30&page=" + str(i)
            request = scrapy.Request(url, callback=self.parse_list)
            yield request

        for j in range(1, 8):
            url = "http://www.comfast.cn/index.php?m=content&c=index&a=lists&catid=31&page=" + str(j)
            request = scrapy.Request(url, callback=self.parse_list)
            yield request


    def parse_list(self, response):
        tr_list = response.xpath(".//tbody[@id='list_cont']/tr")
        for tr in tr_list:
            # self.file_name = tr.xpath("./td[1]/a/text()").extract().pop()
            # self.publishTime = tr.xpath("./td[2]/text()").extract().pop().strip()
            # print self.file_name
            # # print absurl
            # # print publishTime

            href = tr.xpath("./td[3]/a/@href").extract().pop()
            url = urlparse.urljoin(ComfastSpider.headurl, href)
            request = scrapy.Request(url, callback=self.parse_page)
            yield request


    def parse_page(self, response):
        href = response.xpath("/html/body/div[3]/div[2]/div/div/div[2]/div/div[2]/p/a[2]/@href").extract().pop()
        absurl = urlparse.urljoin(ComfastSpider.headurl, href)
        # filename = self.file_name
        # # print filename
        # publishTime = self.publishTime

        filename = response.xpath("/html/body/div[3]/div[2]/div/div/div[2]/div/h1/text()").extract().pop()
        # print filename

        version = re.search("V(.*)", filename)
        if version:
            productVersion = version.group()
        else:
            productVersion = ""
        # print productVersion

        publish_Time = response.xpath("/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/text()").extract().pop().strip()
        publishTime = publish_Time.split(" ")[0]
        # print publishTime


        item = MI.FirmcrawlerItem()
        item["firmwareName"] = filename
        item["publishTime"] = publishTime
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = ""
        item["productClass"] = ""
        item["productVersion"] = productVersion
        item["productModel"] = ""
        item["manufacturer"] = "comfast"

        yield item
        print "firmwarename:", item["firmwareName"]






