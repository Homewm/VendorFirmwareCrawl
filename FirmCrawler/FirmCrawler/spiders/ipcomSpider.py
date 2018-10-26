# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.11"

"""网站地址和网站结构全部发生改变"""

from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time


class ipcomSpider(Spider):
    name = "ipcom"
    timeout = 20
    trytimes = 3

    allowed_domains = ["ip-com.com.cn"]
    start_urls = ["http://www.ip-com.com.cn/en/download/cata-12.html"]

    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()

    headurl = "http://www.ip-com.com.cn/"


    def parse(self, response):
        tr_list = response.xpath('//div[@class="container"]/div/div/table/tr')
        # l = response.xpath('//div[@class="down_content"]/table/tr')    ###不能定位到,原因待审查

        tr_num =  len(tr_list)
        # print tr_num

        for i in range(0, tr_num - 2, 2):
            if i % 2 == 0:
                filename = tr_list[i].xpath('./td[2]/a/text()').extract()[0]
                # print firmwareName

                url = tr_list[i].xpath('./td[2]/a/@href').extract()[0]
                absurl = urlparse.urljoin(ipcomSpider.headurl, url)
                # print absurl

                productVersion = filename.split(" ")[-1]
                # print productVersion

                productModel = filename.split(" ") [0]

                desc = tr_list[i+1].xpath('./td[2]/div/text()').extract()
                desc = " ".join(desc)
                # print desc

            else:
                pass


            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = ""
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = desc
            item["productClass"] = ""
            item["productVersion"] = productVersion
            item["productModel"] = productModel
            item["manufacturer"] = "ip-com"

            yield item

            print "firmwarename:", item["firmwareName"]

        return

