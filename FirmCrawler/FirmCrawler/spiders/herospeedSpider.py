# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.21"

'''代码编写后存在部分问题，只能抓取部分固件'''
'''部分tr内容无法获取'''
'''涉及到链接中的空格，替换为%20'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class HeroSpeedSpider(Spider):
    name = "herospeed"
    start_urls = ["http://www.herospeed.net/en/"]

    allsuffix = Set()
    timeout = 20
    trytimes = 3

    def parse(self, response):
        dd_list = response.xpath(".//*[@id='orderedlist']/dl/dd")
        # print dd_list
        for dd in dd_list:
            href = dd.xpath("./div[4]/a/@href").extract().pop()

            request = scrapy.Request(href, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        # print response.url
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=109（Manual pdf文件，无需下载）
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=15 (XVR2不规则)111
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=16 (Wifi kits4不规则)
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=14 (NVR2不规则)111
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=11 (Hisillicon ip camera4不规则)
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=12 (Ambarella IP Camera 3规则的)
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=13 (Fullhan IP Camera 3规则的)
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=10 (pc1规则的)111
        # http://www.herospeed.net/en/index.php?m=content&c=index&a=lists&catid=24 (tools1规则的)111
        url = response.url
        url_last = url.split("=")[-1]

        productVersion = ""
        productModel = ""
        absurl = ""
        productClass = ""

        if url_last == "10" or url_last == "24" :
            productClass = response.xpath("/html/body/div[4]/h1/text()").extract().pop()
            tr_list = response.xpath("/html/body/div[4]/table/tr[position()>1]")
            for tr in tr_list:
                productModel = tr.xpath("./td[1]/text()").extract().pop()
                productVersion = tr.xpath("./td[2]/text()").extract().pop()
                url = tr.xpath("./td[3]/a/@href").extract().pop()
                absurl = url.replace(" ","%20")
                filename = absurl.split("/")[-1]

                item = MI.FirmcrawlerItem()
                item["firmwareName"] = filename
                item["productVersion"] = productVersion
                item["productModel"] = productModel
                item["productClass"] = productClass
                item["publishTime"] = ""
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absurl
                item["description"] = ""
                item["manufacturer"] = "herospeed"
                yield item
                print "firmwarename:", item["firmwareName"]



        if url_last == "14" or url_last == "15":
            productClass = response.xpath("/html/body/div[4]/h1/text()").extract().pop()
            tr_list = response.xpath("/html/body/div[4]/table/tr[position()>1]")
            # print len(tr_list)
            for tr in tr_list:
                td = tr.xpath("./td")
                if len(td) >=3:
                    productModel = tr.xpath("./td[1]/text()").extract().pop()
                    productVersion = tr.xpath("./td[2]/text()").extract().pop()
                    url = tr.xpath("./td[3]/a/@href").extract().pop()
                    absurl = url.replace(" ", "%20")
                    filename = absurl.split("/")[-1]

                ###此处有问题
                elif len(td) == 2:
                    productVersion = tr.xpath("./td[1]/text()").extract().pop()
                    url = tr.xpath("./td[2]/a/@href").extract().pop()
                    absurl = url.replace(" ", "%20")
                    filename = absurl.split("/")[-1]
                # print filename

                item = MI.FirmcrawlerItem()
                item["firmwareName"] = filename
                item["productVersion"] = productVersion
                item["productModel"] = productModel
                item["productClass"] = productClass
                item["publishTime"] = ""
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absurl
                item["description"] = ""
                item["manufacturer"] = "herospeed"

                yield item
                print "firmwarename:", item["firmwareName"]


        if url_last == "12" or url_last == "13":
            productClass = response.xpath("/html/body/div[4]/h1/text()").extract().pop()
            tr_list = response.xpath("/html/body/div[4]/table/tr[position()>1]")
            for tr in tr_list:
                productModel = tr.xpath("./td[3]/text()").extract().pop()
                url = tr.xpath("./td[4]/a/@href").extract().pop()
                absurl = url.replace(" ","%20")
                filename = absurl.split("/")[-1]
                #
                item = MI.FirmcrawlerItem()
                item["firmwareName"] = filename
                item["productVersion"] = productVersion
                item["productModel"] = productModel
                item["productClass"] = productClass
                item["publishTime"] = ""
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absurl
                item["description"] = ""
                item["manufacturer"] = "herospeed"

                yield item
                print "firmwarename:", item["firmwareName"]




        if url_last == "11" or url_last == "16":
            productClass = response.xpath("/html/body/div[4]/h1/text()").extract().pop()
            tr_list = response.xpath("/html/body/div[4]/table/tr[position()>1]")
            for tr in tr_list:
                try:
                    productModel = tr.xpath("./td[3]/text()").extract().pop()
                    url = tr.xpath("./td[4]/a/@href").extract().pop()
                    absurl = url.replace(" ", "%20")
                    filename = absurl.split("/")[-1]
                except Exception,e:
                    print e.message

                item = MI.FirmcrawlerItem()
                item["firmwareName"] = filename
                item["productVersion"] = productVersion
                item["productModel"] = productModel
                item["productClass"] = productClass
                item["publishTime"] = ""
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absurl
                item["description"] = ""
                item["manufacturer"] = "herospeed"

                yield item
                print "firmwarename:", item["firmwareName"]















