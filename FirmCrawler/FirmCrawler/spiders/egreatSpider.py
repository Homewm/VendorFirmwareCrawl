# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.10"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import re


class EgreatSpider(Spider):
    name = "egreat"
    allowed_domain = ["egreatworld.com"]
    start_urls = [
        "http://www.egreatworld.com/egreat-firmware-download.html"
    ]
    headurl = "http://www.egreatworld.com"

    allsuffix = Set()
    timeout = 20
    trytimes = 3


    def parse(self, response):
        article_list = response.xpath(".//div[@id='portfolio']/article")
        # print len(article_list)
        for article in article_list:
            href = article.xpath("./div/a/@href").extract().pop()
            url = urlparse.urljoin(self.headurl, href)

            request = scrapy.Request(url, callback=self.parse_page)
            yield  request

    def parse_page(self, response):
        # print response.url
        productModel = response.xpath(".//section[@id='page-title']/div/h1/text()").extract().pop().split("固件")[0]
        # print productModel
        div1 = response.xpath(".//div[@id='posts']/div[@class='entry clearfix']")
        # print len(div1)
        div2 = response.xpath(".//div[@id='posts']/div[@class='entry clearfix alt']")
        # print len(div2)
        div = div1+div2
        # print len(div)

        for d in div:
            absurl = d.xpath("./div[2]/div/div/a[1]/@href").extract().pop()
            # print absurl
            filename = d.xpath("./div[2]/div/div/a[1]/text()").extract().pop()
            desc_info = d.xpath("./div[2]/div/div")
            desc_ = desc_info.xpath('string(.)').extract()
            desc = ""
            for description in desc_:
                description_ = description.strip()
                desc = desc + description_

            # print desc
            # print filename
            version = re.search("v\d.+", filename)
            if version:
                productVersion = version.group()
            else:
                productVersion = ""
            # print productVersion
            publish_Time = d.xpath("./div[2]/div/div/div/ul/li[1]/text()").extract().pop()
            publishTime = ""
            try:
                array = time.strptime(publish_Time, u"%Y年%m月%d日")
                publishTime = time.strftime("%Y-%m-%d", array)
            except Exception, e:
                print e

        # print publishTime

            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = desc
            item["productClass"] = ""
            item["productVersion"] = ""
            item["productModel"] = productModel
            item["manufacturer"] = "egreat"

            yield item
            print "firmwarename:", item["firmwareName"]
