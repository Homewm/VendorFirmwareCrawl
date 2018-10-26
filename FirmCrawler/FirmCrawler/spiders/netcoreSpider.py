# -*- coding: UTF-8 -*-

__author__ = "zhangguodong"
__time__ = "2018.09.29"



from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import string
import re
import urlparse
import urllib2
import time

class netcoreSpider(Spider):
    name = "netcore"
    timeout = 20
    trytimes = 3
    start_urls = ["http://www.netcoretec.com/companyfile/2/"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()

    def parse(self, response):
        for i in range(1,14): #13+1
            url_list = "http://www.netcoretec.com/companyfile/2/%23c_companyFile_list-15086754191809347-" + str(i)
            # print url_list
            request = scrapy.Request(url_list, callback=self.parse_list)

            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "netcore"
            yield request

    def parse_list(self, response):
        prototype = response.meta['prototype']
        lines = response.xpath('//div[@id="c_companyFile_list-15086754191809347"]/div/div[1]/div')
        for line in lines:
            filename = line.xpath('./div/div[2]/div[1]/a/h3/div/text()').extract().pop()
            # print filename
            productModel = filename.split("升级")[0]
            # print productModel
            publishTime = line.xpath('./div/div[2]/div[4]/div/div/text()').extract().pop()
            # print publishTime


            ###http://www.netcoretec.com/comp/companyFile/download.do?fid=104&appId=24&id=98
            ###http://www.netcoretec.com/comp/companyFile/download.do?fid=103&appId=24&id=97#
            ###在网页上很难找到这两个参数(使用javascript内容,仔细找找还是能找得到的)
            cid = line.xpath('./div/a/@cid').extract().pop()
            data = line.xpath('./div/a/@data').extract().pop()
            # print cid,data
            absurl = "http://www.netcoretec.com/comp/companyFile/download.do?fid=" + str(cid) + "&appId=24&id=" + str(data)

            item = MI.FirmcrawlerItem(prototype)
            item["firmwareName"] = filename
            item["url"] = absurl
            item["productVersion"] = ""
            item["publishTime"] = publishTime
            item["productClass"] = ""
            item["productModel"] = productModel
            item["description"] = ""
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            yield item
            print "firmwarename:",item["firmwareName"]



