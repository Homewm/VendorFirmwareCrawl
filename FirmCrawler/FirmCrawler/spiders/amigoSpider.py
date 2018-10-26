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


class amigoSpider(Spider):
    name = "amigo"
    start_urls = ["https://www.amigo.cn/down.php"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3
    headurl = "https://www.amigo.cn"


    def parse(self, response):
        div_list = response.xpath("/html/body/section/article[2]/div")
        # print div_list
        for div in div_list:
            div_list_2 = div.xpath('./div')
            for div_2 in div_list_2:
                href = div_2.xpath('./a/@href').extract().pop()
                # print href
                url = urlparse.urljoin(self.headurl, href)

                request = scrapy.Request(url ,callback=self.parse_page)
                yield request

    def parse_page(self, response):
        version = response.xpath('/html/body/section/article[1]/div[3]/div[2]/ul/li[1]/strong/text()').extract().pop()
        publishTime = response.xpath('/html/body/section/article[1]/div[3]/div[2]/ul/li[2]/strong/text()').extract().pop()
        productModel = response.xpath('/html/body/section/article[1]/div[3]/div[1]/ul/li[2]/b/text()').extract().pop()
        filename = productModel
        decription = response.xpath('/html/body/section/article[1]/div[3]/div[2]/ul/li[3]')
        desc = decription.xpath('string(.)').extract().pop()
        absurl = response.xpath('/html/body/section/article[1]/div[3]/div[3]/a[1]/@href').extract().pop()


        item = MI.FirmcrawlerItem()
        item["firmwareName"] = filename
        item["productVersion"] = version
        item["productModel"] = productModel
        item["productClass"] = "phone"
        item["publishTime"] = publishTime
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = desc
        item["manufacturer"] = "amigo"

        yield item
        print "firmwarename:", item["firmwareName"]
