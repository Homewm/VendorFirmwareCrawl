# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.26"


'''代理ip不能使用,去除后正常'''


from scrapy import Spider
from scrapy.http import Request
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import urlparse
import time
from proxy_ips import proxy_ip
import random


# def random_proxy_ip():
#     proxy_ip_index = random.randint(0,len(proxy_ip)-1)
#     #res = {'http':proxy_ip[proxy_ip_index]}
#     res = proxy_ip[proxy_ip_index]
#     return res


class XeroxSpider(Spider):
    name = "xerox"
    allowed_domains = ["xerox.com"]
    start_urls = ["http://www.support.xerox.com/dnd/productList.jsf?Xlang=en_US"]

    def parse(self, response):
        # iprand = random_proxy_ip()
        # print "random proxy:", iprand
        for href in response.xpath("//div[@class='productResults a2z']//a/@href").extract():
            if "downloads" in href:
                # callback=self.parse_download,meta={'proxy':'http://'+iprand})
                yield Request(
                    url=urlparse.urljoin(response.url, href),
                    headers={"Referer": response.url},
                    callback = self.parse_download)

    def parse_download(self, response):
        for firmware in response.xpath(
                "//li[@class='categoryBucket categoryBucketId-7']//li[@class='record ']"):
            product = response.xpath(
                "//div[@class='prodNavHeaderBody']//text()").extract()[0].replace(" Support & Drivers", "")
            date = firmware.xpath(
                ".//ul[@class='dateVersion']//strong/text()").extract()
            version = firmware.xpath(
                ".//ul[@class='dateVersion']//strong/text()").extract()
            href = firmware.xpath(
                ".//a/@href").extract()[0].replace("file-download", "file-redirect")
            absurl = urlparse.urljoin(response.url,href)
            text = firmware.xpath(".//a//text()").extract()[0]

            item = FirmcrawlerItem()
            item["productVersion"] = FirmwareLoader(date_fmt=["%Y-%m-%d"]).find_version_period(version)
            item["publishTime"] = ""
            item["productClass"] = "printer"
            item["productModel"] = product
            item["description"] = text
            item["url"] = absurl
            item["firmwareName"] = "xerox-" + absurl.split('=')[-1]
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["manufacturer"] = "xerox"
            yield item
            print "firmwarename:", item["firmwareName"]




