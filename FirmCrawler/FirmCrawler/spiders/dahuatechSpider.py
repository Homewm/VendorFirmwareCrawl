# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.07"


from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import re


class DaHuaSpider(Spider):
    name = "dahuatech"
    allowed_domain = ["www.dahuatech.com"]
    start_urls = ["https://www.dahuatech.com/service/download.html"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    def parse(self, response):
        div_list = response.xpath('//html/body/div[1]/div[2]/div/div[2]/ul/li[2]/div[position()<3]')
        for div_in in div_list:
            href_list = div_in.xpath('./div/a/@href').extract()
            for href in href_list:
                request = scrapy.Request(href, callback=self.parse_list)
                request.meta["prototype"] = MI.FirmcrawlerItem()
                request.meta["prototype"]["manufacturer"] = "dahuatech"
                yield request

    def parse_list(self, response):
        property = response.meta['prototype']
        productClass = response.xpath('//html/body/div[1]/div[2]/div[3]/text()').extract().pop()
        # print productClass
        li_list = response.xpath('//html/body/div[1]/div[2]/div[4]/ul/li')
        for li_info in li_list:
            filename = li_info.xpath('./div[2]/dl/dd/h2/text()').extract().pop()
            # print filename
            version = re.search("V\d.+.bin", filename)
            if version:
                product_Version = version.group()
                productVersion = product_Version.split(".bin")[0]
            else:
                productVersion = ""

            absurl = li_info.xpath('./div[2]/dl/dd/div[2]/a/@href').extract().pop()


            desc_info = li_info.xpath('./div[2]/dl/dd/div[1]/p[position()>2]/span/text()').extract()
            if desc_info:
                desc = "".join(desc_info)
            else:
                desc = ""

            item = MI.FirmcrawlerItem(property)
            item["firmwareName"] = filename
            item["publishTime"] = ""
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = ""
            item["productClass"] = productClass
            item["productVersion"] = productVersion
            item["productModel"] = ""
            # item["manufacturer"] = "dahuatech"

            yield item
            print "firmwarename:", item["firmwareName"]







