# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.09"


from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class UniviewSpider(Spider):
    name = "uniview"
    allowed_domain = ["cn.uniview.com"]
    start_urls = [
        "http://cn.uniview.com/Service/Service_Training/Download/Tools/"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3
    headurl = "http://cn.uniview.com"


    def parse(self, response):
        li_list = response.xpath(".//div[@id='detailContent']/div/ul/li")
        # print len(li_list)
        for li in li_list:
            publish_Time = li.xpath("./a/span/text()").extract().pop()
            self.publishTime = publish_Time.split("[")[-1].split("]")[0]
            # print publishTime

            self.productModel = li.xpath("./a/text()").extract().pop()
            # print productModel

            href = li.xpath("./a/@href").extract().pop()
            url = urlparse.urljoin(self.headurl, href)
            request = scrapy.Request(url, callback=self.parse_list)
            yield request


    def parse_list(self, response):
        table_list = response.xpath(".//div[@id='wrapper']/div[3]/div/div[1]/div/div[1]/table")
        for table in table_list:
            filename = table.xpath("./tbody/tr[1]/td/text()").extract().pop()
            href = table.xpath("./tbody/tr[1]/td/a/@href").extract().pop()
            absurl = urlparse.urljoin(self.headurl, href)
            description = table.xpath("./tbody/tr[2]/td/text()").extract()
            desc = " ".join(description)


            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = self.publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = desc
            item["productClass"] = ""
            item["productVersion"] = ""
            item["productModel"] = self.productModel
            item["manufacturer"] = "uniview"

            yield item
            print "firmwarename:", item["firmwareName"]







    #     for page in xrange(1,5):
    #         url_router = "http://www.wayos.com/download/luyougujian/" + str(page) + ".html"
    #         request = scrapy.Request(url_router, callback=self.parse_list)
    #
    #         request.meta["prototype"] = MI.FirmcrawlerItem()
    #         request.meta["prototype"]["manufacturer"] = "Wayos"
    #         yield request
    #
    #     for page in xrange(1, 3):
    #         url_app = "http://www.wayos.com/download/APgujian/" + str(page) + ".html"
    #         request = scrapy.Request(url_app, callback=self.parse_list)
    #
    #         request.meta["prototype"] = MI.FirmcrawlerItem()
    #         request.meta["prototype"]["manufacturer"] = "Wayos"
    #         yield request
    #
    #
    # def parse_list(self, response):
    #     page_url = response.url
    #
    #     li_list = response.xpath('//div[@class="download"]/div[1]/li')
    #     for li in li_list:
    #         filename = li.xpath('./a/text()').extract().pop()
    #         absurl = li.xpath('./a/@href').extract().pop()
    #         publishTime = li.xpath('./span/text()').extract().pop()
    #         # print publishTime
    #
    #         productVersion = filename.split("-")[-1].split("固件")[0]
    #         # print version
    #
    #         product_class = page_url.split("/")[-2]
    #         # print product_class
    #         if "luyou" in product_class:
    #             productClass = "router"
    #         elif "APgujian" in product_class:
    #             productClass = "app"
    #         else:
    #             productClass = ""
    #         # print productClass
    #
    #         productModel = filename.rsplit("-", 1)[0]
    #         # print productModel
    #
    #         item = MI.FirmcrawlerItem()
    #         item["firmwareName"] = filename
    #         item["publishTime"] = publishTime
    #         item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
    #         item["url"] = absurl
    #         item["description"] = ""
    #         item["productClass"] = productClass
    #         item["productVersion"] = productVersion
    #         item["productModel"] = productModel
    #         item["manufacturer"] = "wayos"
    #
    #         yield item
    #         print "firmwarename:", item["firmwareName"]
    #
    #
    #




