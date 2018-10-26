# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2019.09.25"

from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time



class adslrSpider(Spider):
    name = "adslr"
    timeout = 20
    trytimes = 3
    start_urls = [
        "http://www.adslr.com/down/gjsj/index.html",
        "http://www.adslr.com/down/gjsj/index_2.html",
        "http://www.adslr.com/down/gjsj/index_3.html",
        # "http://www.adslr.com/down/gjhf/"
    ]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    headurl = "http://www.adslr.com/"

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "adslr"
        yield request

    def parse_page(self, response):
        href_list = response.xpath('//div[@id="right"]/div/div[2]/ul/li/table/tr[position()>1]/td[1]/a/@href').extract()
        for href in href_list:
            url = urlparse.urljoin(adslrSpider.headurl, href)
            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "adslr"
            yield request

    def parse_list(self, response):
        prototype = response.meta['prototype']

        file_name1 = response.xpath('//div[@id="right"]/ul/table/tr[1]/td[2]/i/text()').extract().pop()

        productModel = file_name1.split("固件")[0]
        publish_Time = response.xpath('//div[@id="right"]/ul/table/tr[5]/td[2]/i/text()').extract().pop()
        publishTime = publish_Time.split()[0]
        # print publishTime

        ###注意存在p的时候,txtear是否有用
        file_name2 = response.xpath('//div[@id="right"]/ul/table/tr[6]/td[2]/p[1]/text()').extract()
        file_name3 = response.xpath('//div[@id="right"]/ul/table/tr[6]/td[2]/p/text()').extract()
        if file_name2:
            filename = file_name2.pop().strip()
        elif file_name3:
            filename = file_name3.pop().srtip()
        else:
            filename = file_name1
        # print filename

        desc = response.xpath('//div[@id="right"]/ul/table/tr[6]/td[2]/p[position()>1]/text()').extract()
        description = " ".join(desc)
        # print description

        ##注意li是否有用
        url = response.xpath('//div[@id="right"]/ul/table/tr[2]/td[2]/a/@href').extract().pop()
        # print "url:",url
        url_last = url.split("/")[-1]
        # print "last:",url_last

        if "download" in url_last:
            absurl = url
        elif ".bin" in url_last:
            absurl = url
        else:
            absurl = url + "/download"
        # print absurl


        item = MI.FirmcrawlerItem(prototype)
        item["firmwareName"] = filename
        item["publishTime"] = publishTime
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = description
        item["productClass"] = ""
        item["productVersion"] = ""
        item["productModel"] = productModel
        # item["manufacturer"] = "adslr"

        yield item
        print "firmwarename:", item["firmwareName"]
        # print "publishTime:", item["publishTime"]
        # print "crawlerTime:",item["crawlerTime"]
        # print "url:",item["url"]
        # print "description:", item["description"]
        # print "productModel:", item["productModel"]
        print item["manufacturer"]