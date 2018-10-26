# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.29"

'''网站结构发生变化,代码重写后正常使用'''

from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time


class schnerderSpider(Spider):
    name = "schneider"
    timeout = 20
    trytimes = 3
    start_urls = ["https://www.schneider-electric.cn/zh/download/search/?docTypeGroup=4868253-软件/固件"]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    headurl = "https://www.schneider-electric.cn/"


    def parse(self, response):
        # for i in xrange(1,10):
        #     url = "https://www.schneider-electric.cn/zh/download/search/?docTypeGroup=4868253-软件%2F固件&docType=1555893-固件-发布&pageNumber=" + str(i)
        #
        #     request = scrapy.Request(url, callback=self.parse_list)
        #     request.meta["prototype"] = MI.FirmcrawlerItem()
        #     request.meta["prototype"]["manufacturer"] = "schneider"
        #     yield request

        for i in xrange(1,14):
            url = "https://www.schneider-electric.cn/zh/download/search/?docTypeGroup=4868253-软件%2F固件&docType=1555902-固件-更新&pageNumber=" + str(i)

            request = scrapy.Request(url, callback=self.parse_list)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "schneider"
            yield request

    def parse_list(self, response):
        prototype = response.meta['prototype']
        href_list = response.xpath('//div[@id="main-content"]/div[2]/div[2]/div[2]/ul/li/div/section/a/@href').extract()
        for href in href_list:
            url = urlparse.urljoin(schnerderSpider.headurl, href)

            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = MI.FirmcrawlerItem()
            request.meta["prototype"]["manufacturer"] = "schneider"
            yield request

    def parse_page(self, response):
        prototype = response.meta['prototype']
        filename = response.xpath('//div[@id="title"]/h1/text()').extract().pop()
        # print filename

        version = response.xpath('.//div[@id="preview-content"]/div[2]/div/ul/li[5]/p/text()').extract()
        if version:
            productVersion = version.pop()
        else:
            productVersion = ""

        publish_Time = response.xpath('.//div[@id="preview-content"]/div[2]/div/ul/li[4]/p/text()').extract()
        if publish_Time:
            publish_Time = publish_Time.pop()
            try:
                array = time.strptime(publish_Time, u"%d/%m/%Y")
                publishTime= time.strftime("%Y-%m-%d", array)
            except Exception, e:
                print e.message
        else:
            publishTime = ""

        desc = response.xpath('//div[@id="preview-content"]/div[2]/div/ul/li[1]/p/text()').extract().pop()
        desc = "样本号:" + desc

        href = response.xpath('.//div[@id="preview-content"]/div[3]/a[1]/@href').extract()
        if href:
            href = href.pop()
            absurl = urlparse.urljoin(schnerderSpider.headurl, href)
        else:
            absurl = ""


        item = MI.FirmcrawlerItem(prototype)

        item["firmwareName"] = filename
        item["url"] = absurl
        item["productVersion"] = productVersion
        item["publishTime"] = publishTime
        item["productClass"] = ""
        item["productModel"] = ""
        item["description"] = desc
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        yield item

        print "firmwaname:",item["firmwareName"]

        return









    #     tables = response.xpath('//li[@class="single-result"]/h3/a/@href').extract()
    #     for t in tables:
    #         url = urlparse.urljoin(response.url,t)
    #         request = scrapy.Request(url, callback=self.parse_page)
    #         request.meta["prototype"] = MI.FirmcrawlerItem()
    #         request.meta["prototype"]["manufacturer"] = "schneider"
    #         yield request
    # def parse_page(self,response):
    #     prototype = response.meta['prototype']
    #     item = MI.FirmcrawlerItem(prototype)
    #     filedownloadlist = response.xpath('//div[@class="description-download lg"]/ul[@class="list-files"]/li/a/@href').extract()
    #     for f in filedownloadlist:
    #         filename = f.split('p_File_Name=')[-1].split('&')[0]
    #         filetype = filename.rsplit('.',1)[-1]
    #         if filetype not in schnerderSpider.typefilter:
    #             url = f
    #             model = filename.split('_')[0]
    #             publishtime = response.xpath('//ul[@class="detail"]/li[4]/p/text()').extract().pop()
    #             version = response.xpath('//ul[@class="detail"]/li[5]/p/text()').extract().pop()
    #             desc = response.xpath('//div[@class="description-download lg"]/p[1]//text()').extract()
    #             try:
    #                 array = time.strptime(publishtime, u"%d/%m/%Y")
    #                 item["publishTime"] = time.strftime("%Y-%m-%d", array)
    #             except Exception, e:
    #                 print e
    #             item["productVersion"] = version
    #             item["productClass"] = ""  # more class
    #             item["productModel"] = model
    #             item["description"] = str().join(desc).strip().replace(" ","").replace('\n',"").replace('\t',"")
    #             item["url"] = url
    #             item["firmwareName"] = filename
    #             item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
    #             yield item
    #             print "firmwaname:",item["firmwareName"]
    #     return
    #
