# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.26"


from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time


class xmSpider(Spider):
    name = "xiongmai"
    timeout = 20
    trytimes = 20
    start_urls = [
        "http://www.xiongmaitech.com/index.php/service/down/13"
    ]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()

    '''
    NVR固件（YK风格）------5页
    http://www.xiongmaitech.com/service/down_detail1/13/339
    
    DVR固件（中性风格）------8页
    http://www.xiongmaitech.com/service/down_detail1/13/338
    
    XMJP----8页
    http://www.xiongmaitech.com/index.php/service/down_detail1/13/170
    
    IPC-----18页
    http://www.xiongmaitech.com/index.php/service/down_detail1/13/2
    
    DVR------4页
    http://www.xiongmaitech.com/service/down_detail1/13/1
    
    NVR------7页
    http://www.xiongmaitech.com/index.php/service/down_detail1/13/4
    '''

    def parse(self, response):
        for p in xrange(1,5+1):
            urls = "http://www.xiongmaitech.com/index.php/service/down_detail1/13" + "/339/" + str(p)

            request = scrapy.Request(urls, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["productClass"] = "NVR固件（YK风格）"
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request

        for p in xrange(1,8+1):
            urls = "http://www.xiongmaitech.com/index.php/service/down_detail1/13" + "/338/" + str(p)
            request = scrapy.Request(urls, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["productClass"] = "DVR固件（中性风格）"
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request

        for p in xrange(1,8+1):
            urls = "http://www.xiongmaitech.com/index.php/service/down_detail1/13" + "/170/" + str(p)
            request = scrapy.Request(urls, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["productClass"] = "XMJP"
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request

        for p in xrange(1,18+1):
            urls = "http://www.xiongmaitech.com/index.php/service/down_detail1/13" + "/2/" + str(p)
            request = scrapy.Request(urls, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["productClass"] = "IPC"
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request

        for p in xrange(1, 4+1):
            urls = "http://www.xiongmaitech.com/index.php/service/down_detail1/13" + "/1/" + str(p)
            request = scrapy.Request(urls, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["productClass"] = "DVR固件（YK风格）"
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request

        for p in xrange(1, 7+1):
            urls = "http://www.xiongmaitech.com/index.php/service/down_detail1/13" + "/4/" + str(p)
            request = scrapy.Request(urls, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["productClass"] = "NVR固件（中性风格）"
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request


    def parse_list(self, response):
        prototype = response.meta['prototype']
        href_list = response.xpath('//div[@class="w1000"]/div/div[2]/ul/li/a/@href').extract()
        # print href_list

        if len(href_list) == 0:
            urls = response.url
            request = scrapy.Request(urls, callback=self.parse_list)
            # print urls
            request.meta["prototype"] = response.meta["prototype"]
            yield request

        else:
            for href in href_list:
                url = href
                request = scrapy.Request(url, callback=self.parse_page)
                request.meta["prototype"] = MI.FirmcrawlerItem()
                request.meta["prototype"]["manufacturer"] = "xiongmai"
                yield request


    def parse_page(self, response):
        prototype = response.meta['prototype']
        version = response.xpath('//div[@class="down1-ccont"]/div[2]/p[1]/text()').extract()
        if version:
            self.productVersion = version[0]
        else:
            self.productVersion = ""


        description = response.xpath('//div[@class="down1-ccont"]/div[2]/p[position()>1]/text()').extract()
        if description:
            self.desc = " ".join(description)
        else:
            self.desc = ""


        urls = response.xpath('//div[@class="down1-ccont"]/div[2]/p[1]/a/@href').extract()
        if urls:
            url = urls[0]
            request = scrapy.Request(url, callback=self.parse_next)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "xiongmai"
            yield request


    def parse_next(self, response):

        prototype = response.meta['prototype']

        productVersion = self.productVersion
        # print productVersion
        desc = self.desc
        # print desc
        filename = response.xpath('/html/body/div[2]/table/tr[4]/td/text()').extract().pop()
        publishTime = response.xpath('/html/body/div[2]/table/tr[3]/td/text()').extract().pop()

        product_Model = response.xpath('/html/body/div[2]/table/tr[2]/td/text()').extract()
        if product_Model:
            productModel = product_Model.pop()
        else:
            productModel = ""
        # print productModel

        absurl = response.xpath('/html/body/div[2]/table/tr[5]/td/div[1]/a/@href').extract().pop()
        # print absurl

        # # print publishTime
        #
        item = MI.FirmcrawlerItem(prototype)
        item["firmwareName"] = filename
        item["publishTime"] = publishTime
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = desc
        # item["productClass"] = productClass
        item["productVersion"] = productVersion
        item["productModel"] = productModel
        # item["manufacturer"] = "xiongmai"

        yield item
        print "firmwarename:", item["firmwareName"]









        # urls = response.xpath('//div[@class="down1-ccont"]//a[1]/@href').extract() #soho pan url
        # if urls:
        #
        #     # print "urls:",urls[0]
        #     infos = response.xpath('//div[@class="down-p2"]/p/text()').extract()[0]
        #     infos = unicode.encode(infos, encoding='utf8')
        #     # print "infos:",infos
        #     if "最新固件" in infos:
        #         model = infos.split("(")[-1].split(")")[0]
        #         version = response.xpath('//div[@class="down1-ccont"]/p[1]/text()').extract()[0]
        #         # print "dn version:",version
        #         version = version.split(":")[-1]
        #     else:
        #         version = infos.rsplit("_",1)[-1]
        #         model = infos.rsplit("_",1)[0].split(")")[-1]
        #
        #
        #     item = MI.FirmcrawlerItem()
        #     item["productVersion"] = version
        #     item["productClass"] = "Camera"
        #     item["productModel"] = model
        #     item["description"] = ""
        #     item["url"] = urls[0]
        #     item["firmwareName"] = item["url"].split("/")[-1]
        #     item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        #     item["manufacturer"] = "xiongmai"
        #     #yield item
        #     print "firmware name:", item["firmwareName"]



