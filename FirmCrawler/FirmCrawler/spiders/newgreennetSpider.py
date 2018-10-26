# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.09"


from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import re

'''代码写后正常使用'''

class NewgreennetSpider(Spider):
    name = "newgreennet"
    allowed_domain = ["newgreennet.com"]
    start_urls = [
        "http://www.newgreennet.com/category.aspx?SiteID=27564&NodeID=90&page=1"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 5
    headurl = "http://www.newgreennet.com"


    def parse(self, response):
        for page in range(1,3):
            url = "http://www.newgreennet.com/category.aspx?SiteID=27564&NodeID=90&page=" + str(page)
            request = scrapy.Request(url, callback=self.parse_page)
            yield request


    def parse_page(self, response):
        li_list = response.xpath("//html/body/div[1]/div[3]/div[1]/div[2]/div/ul/li")
        for li in li_list:
            filename = li.xpath("./h3/a/text()").extract().pop().strip()
            href = li.xpath("./h3/a/@href").extract().pop()
            absurl = urlparse.urljoin(self.headurl, href)

            description = li.xpath("./p[2]/text()").extract()
            if description:
                desc = description.pop()
            else:
                desc = ""

            product_Model = desc.split(" ")[0]
            if product_Model:
                productModel = product_Model
            else:
                productModel = ""

            publish_Time = desc.split(" ")[-1]
            if publish_Time:
                publish_Time_ = re.search("\d.+.\d", publish_Time)
                if publish_Time_:
                    publishTime = publish_Time_.group()
            else:
                publishTime = ""
            # print publishTime

            version_info = re.search("V.*", desc)
            if version_info:
                version = version_info.group()
                productVersion = version.split(" ")[0]
            else:
                productVersion = ""

            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = ""
            item["productClass"] = ""
            item["productVersion"] = productVersion
            item["productModel"] = productModel
            item["manufacturer"] = "newgreennet"

            yield item
            print "firmwarename:", item["firmwareName"]







