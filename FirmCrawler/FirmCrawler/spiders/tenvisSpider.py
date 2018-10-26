# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.18"

'''代理ip存在问题,代码修改后正常使用'''

from scrapy import Spider
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import time
from proxy_ips import proxy_ip
import random
import scrapy

# def random_proxy_ip():
#     proxy_ip_index = random.randint(0,len(proxy_ip)-1)
#     #res = {'http':proxy_ip[proxy_ip_index]}
#     res = proxy_ip[proxy_ip_index]
#     return res

class Tenvispider(Spider):
    name = "tenvis"
    allowed_domains = ["tenvis.com"]
    start_urls = ["http://forum.tenvis.com/viewtopic.php?f=13&t=3233"]

    # from the image
    # http://forum.tenvis.com/download/file.php?id=6163&sid=cfffb0412651f05728623840e8fc5584&mode=view
    firmware = [("JPT3815W, JPT3815W+", "0.22.2.34"),
                ("JPT3815W, JPT3815W+", "0.37.2.36"),
                ("JPT3815W, JPT3815W+", "32.37.2.39"),
                ("JPT3815W, JPT3815W+", "1.7.25"),
                ("JPT3815W, JPT3815W+", "1.7.25"),
                ("JPT3815W, JPT3815W+", "1.7.25"),
                ("JPT3815W, JPT3815W+", None),
                ("JPT3815W, JPT3815W+", None),
                ("JPT3815W P2P, TR3818/TR3828", "3.1.1.1.4"),
                ("ROBOT2", "0.22.2.34"),
                ("ROBOT2", "0.37.2.36"),
                ("ROBOT2", "32.37.2.39"),
                ("ROBOT2", "3.1.1.1.4"),
                ("391W", "0.22.2.34"),
                ("391W", "0.37.2.36"),
                ("391W", "32.37.2.39"),
                ("391W", "3.7.25"),
                ("391W", "3.7.25"),
                ("391W", "5.1.1.1.5"),
                ("602W", "0.22.2.34"),
                ("602W", "0.37.2.36"),
                ("602W", "32.37.2.39"),
                ("602W", "3.7.25"),
                ("602W", "3.7.25"),
                ("602W", "5.1.1.1.5"),
                ("MINI319", "0.22.2.34"),
                ("MINI319", "0.37.2.36"),
                ("MINI319", "32.37.2.39"),
                ("MINI319", "2.7.25"),
                ("MINI319", "2.7.25"),
                ("MINI319", "2.7.25"),
                ("MINI319", "12.1.1.1.2"),
                ("ROBOT3", "1.3.3.3"),
                ("ROBOT3", "1.2.7.2"),
                ("ROBOT3", "1.2.1.4"),
                ("ROBOT3", "7.1.1.1.1.2"),
                ("ROBOT3", None),
                ("391W HD", "1.3.3.3"),
                ("391W HD", "1.2.7.2"),
                ("TH671", "8.1.1.1.1.2"),
                ("TH692", None),
                ("TH661", "7.1.1.1.1.2"),
                ("TH661", None),
                ("JPT3815W HD", None),
                ("JPT3815W HD", None)]


    def parse(self,response):
        # iprand = random_proxy_ip()
        # print "random proxy:", iprand
        # request=scrapy.Request(response.url, callback=self.parse_page,meta={'proxy':'http://'+iprand})
        request = scrapy.Request(response.url, callback=self.parse_page)
        yield request

    def parse_page(self, response):
        for entry in response.xpath("//div[@class='content']//a"):
            text = entry.xpath(".//text()").extract()
            href = entry.xpath("./@href").extract()[0]
            item = FirmcrawlerItem()
            if len(text):
                if "---" in text[0]:
                    version = text[0].split("-")[-1]
                    item["productVersion"] = version
                    item["publishTime"] = ""
                    item["productClass"] = "camera"
                    item["productModel"] = ""
                    item["description"] = ""
                    item["url"] = href.replace("(", "%28").replace(")", "%29")
                    item["firmwareName"] = href.split('/')[-1]
                    item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    item["manufacturer"] = "tenvis"
                    yield item
                    print "firmware name:", item["firmwareName"]




