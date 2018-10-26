# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.15"

'''
    1.代码编写后基本正常使用，能爬取绝大多数的固件。
    2.但是存在小的异常，问题仍未解决。未解决的问题写在了博客上。还在咨询中。
'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import string


class KoolShareSpider(Spider):
    name = "koolshare"
    allowed_domain = ["koolshare.cn"]
    start_urls = [
        "http://firmware.koolshare.cn/"
    ]

    allsuffix = Set()
    timeout = 10
    trytimes = 3
    headurl = ""


    def parse(self, response):
        tr_list = response.xpath(".//*[@id='page-content']/div[2]/div[3]/table/tbody/tr")
        for tr in tr_list:
            href = tr.xpath("./td/a/@href").extract().pop()
            file_stype = tr.xpath("./td/a/text()").extract().pop()

            # print "-----", file_stype
            # print href

            request = scrapy.Request(href, meta = {'file_stype':file_stype}, callback=self.parse_list)
            yield request


    def parse_list(self, response):
        file_stype = response.meta['file_stype']
        tr_list_1 = response.xpath(".//*[@id='page-content']/div[2]/div[3]/table/tbody/tr[position()>1]")
        tr_list_2 = response.xpath(".//*[@id='page-content']/div[2]/div[2]/table/tbody/tr[position()>1]")
        if tr_list_1:
            for tr in tr_list_1:
                productModel = tr.xpath("./td[1]/a/text()").extract().pop()
                # print "----------"+response.meta['file_stype']
                # # print productModel

                href = tr.xpath("./td[1]/a/@href").extract().pop()

                request = scrapy.Request(href, meta={'file_stype':file_stype, 'productModel': productModel}, callback=self.parse_page)
                yield request


        else:
            for tr in tr_list_2:
                productModel = tr.xpath("./td[1]/a/text()").extract().pop()
                # print "----------" + response.meta['file_stype']
                # print productModel
                href = tr.xpath("./td[1]/a/@href").extract().pop()
                request = scrapy.Request(href, meta={'file_stype':file_stype, 'productModel': productModel}, callback=self.parse_page)
                yield request


    def parse_page(self, response):
        file_stype = response.meta['file_stype']
        productModel = response.meta['productModel']
        tr_list_1 = response.xpath(".//*[@id='page-content']/div[2]/div[3]/table/tbody/tr[position()>1]")
        tr_list_2 = response.xpath(".//*[@id='page-content']/div[2]/div[2]/table/tbody/tr[position()>1]")
        tr_list = tr_list_1 +tr_list_2

        if tr_list_1:
            for tr in tr_list:
                try:

                    href = tr.xpath("./td[1]/a/@href").extract().pop()

                    if href.endswith('/'):
                        request = scrapy.Request(href, meta={'file_stype':file_stype, 'productModel': productModel}, callback=self.parse_page)
                        yield request

                    else:
                        filename = tr.xpath("./td[1]/a/text()").extract().pop()

                        publish_Time = response.xpath(".//*[@id='page-content']/div[2]/div[3]/table/tbody/tr[1]/td[3]/text()").extract()
                        if publish_Time:
                            publishTime = publish_Time.pop().strip().split()[0]
                        else:
                            publishTime = ""

                        absurl = href


                        item = MI.FirmcrawlerItem()
                        item["firmwareName"] = filename
                        item["publishTime"] = publishTime
                        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        item["url"] = absurl
                        item["description"] = ""
                        item["productClass"] = ""
                        item["productVersion"] = ""
                        item["productModel"] = productModel
                        item["manufacturer"] = "koolshare"

                        yield item
                        print "firmwarename:", item["firmwareName"]


                except Exception,e:
                    print e.message