# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.09"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class UniviewSpider(Spider):
    name = "tiandy"
    allowed_domain = ["tiandy.com"]
    start_urls = [
        "http://www.tiandy.com/tools-pc",
        "http://www.tiandy.com/tools-mobile"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3
    headurl = "http://www.tiandy.com"

    def parse(self, response):
        table_list = response.xpath("//html/body/div[3]/div/div[2]/table")
        for table in table_list:
            #html/body/div[3]/div/div[2]/table[1]/tbody/tr[1]/td[1]/strong
            filename = table.xpath("./tbody/tr[1]/td[1]/strong/text()").extract().pop()

            description = table.xpath("./tbody/tr[2]/td/p/text()").extract()
            desc = ""
            for d in description:
                desc = desc + d.strip()
            # print desc

            absurl = table.xpath("./tbody/tr[1]/td[2]/strong/a/@href").extract().pop()
            # print absurl
            #http://www.tiandy.com/wp-content/files/Easy7SmartClientProfessionalV7.14T.zip


            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = ""
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = desc
            item["productClass"] = ""
            item["productVersion"] = ""
            item["productModel"] = ""
            item["manufacturer"] = "tiandy"

            yield item
            print "firmwarename:", item["firmwareName"]
