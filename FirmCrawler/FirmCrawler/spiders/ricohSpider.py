# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.15"

'''代码编写后正常使用'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse


class RicohSpider(Spider):
    name = "ricoh"
    allowed_domain = ["www.ricoh-imaging.com.cn"]
    start_urls = [
        "http://www.ricoh-imaging.com.cn/ricoh/service_download.html"
    ]

    allsuffix = Set()
    timeout = 20
    trytimes = 3
    headurl = "http://www.ricoh-imaging.com.cn/"


    def parse(self, response):

        tr_list_1 = response.xpath(".//*[@id='content2']/div[4]/table[1]/tr[position()>1]")
        tr_list_2 = response.xpath(".//*[@id='content2']/div[4]/table[2]/tr[position()>1]")
        tr_list = tr_list_1 + tr_list_2

        for tr in tr_list:

            href = tr.xpath("./td[2]/a/@href").extract().pop()
            url = urlparse.urljoin(self.headurl, href)

            prduct_Version = tr.xpath("./td[3]/text()").extract()

            if prduct_Version:
                productVersion = prduct_Version.pop()
            else:
                productVersion = ""

            productModel = tr.xpath("./td[1]/text()").extract().pop()

            desc = tr.xpath("./td[2]/a/text()").extract().pop()

            request = scrapy.FormRequest(url, callback=self.parse_page,
                                     meta={'productModel': productModel, 'productVersion': productVersion, 'desc': desc})
            yield request

    #         request = scrapy.FormRequest(url, callback=lambda response, pm = productModel,pv= productVersion,dc = desc : self.parse_page(response, pm, pv, dc), dont_filter=True)
    #         yield request
    #
    #
    # def parse_page(self, response, pm, pv , dc ):
    #     print pm,pv,dc

    def parse_page(self, response):
        # print response.url
        productModel = response.meta['productModel']
        productVersion = response.meta['productVersion']
        desc = response.meta['desc']

        publish_Time = response.xpath(".//*[@id='content2']/div[4]/div[3]/table/tbody/tr[4]/td[2]/p/span[1]/text()").extract()
        if publish_Time:
            publishTime = publish_Time.pop()
        else:
            publishTime = ""

        href = response.xpath(".//*[@id='content2']/div[4]/div[5]/a[1]/@href").extract()
        if href:
            url = href.pop()
            absurl = urlparse.urljoin(self.headurl, url)
        else:
            absurl = ""

        filename = absurl.split("=")[-1]

        # description = response.xpath(".//div[@id='content2']/div[4]/div[3]")
        # desc_ = description.xpath("string(.)").extract()
        # desc = ""
        # for d in desc_:
        #     desc = desc + d.strip("\n").strip("\t").strip()

        item = MI.FirmcrawlerItem()
        item["firmwareName"] = filename
        item["publishTime"] = publishTime
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["url"] = absurl
        item["description"] = desc
        item["productClass"] = "camera"
        item["productVersion"] = productVersion
        item["productModel"] = productModel
        item["manufacturer"] = "ricoh"

        yield item
        print "firmwarename:", item["firmwareName"]
