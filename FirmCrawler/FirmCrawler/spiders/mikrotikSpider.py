# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.10.22"

'''代码完全重写后正常使用。网站结构发生全面变化'''

from scrapy import Spider
from scrapy.http import FormRequest
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import urlparse
import time


class MikrotikSpider(Spider):
    name = "mikrotik"
    allowed_domains = ["mikrotik.com"]
    start_urls = ["http://www.mikrotik.com/download"]

    def parse(self, response):
        table_list = response.xpath(".//*[@id='sm-start']/div[4]/div/table[@ class='table downloadTable']")
        for table in table_list:
            tr_list1 = table.xpath("./tbody/tr[@class='hv']")
            tr_list2 = table.xpath("./tbody/tr[@class='']")
            tr_list = tr_list1 + tr_list2
            for tr in tr_list:
                td_list = tr.xpath("./td[position()>1]")
                for td in td_list:
                    href = td.xpath("./a/@href").extract().pop()
                    if href.startswith("//"):
                        #https://download2.mikrotik.com/swos/1.17/swos-rb250-1.17.lzb
                        url = "https:" + href
                    else:
                        url = href
                    print url

                    if url:
                        absurl = url
                        filename = url.split("/")[-1]
                        version = url.split("/")[-2]
                        product_class = url.split("/")[-3]

                        productClass = ""
                        if "swos" in product_class:
                            productClass = "switch"
                        elif "routeros" in product_class:
                            productClass = "router"

                        # print filename
                        # print version
                        # print productClass
                        # print absurl

                        item = FirmcrawlerItem()
                        item["productVersion"] = version
                        item["productModel"] = ""
                        item["description"] = ""
                        item["productClass"] = productClass
                        item["url"] = absurl
                        item["firmwareName"] = filename
                        item["publishTime"] = ""
                        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        item["manufacturer"] = "mikrotik"
                        yield item
                        print "firmwarename:",item["firmwareName"]


