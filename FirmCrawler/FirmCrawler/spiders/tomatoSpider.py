#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2017.04.10"

from scrapy import Spider
from scrapy.http import Request
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import os
import urlparse
import time

class TomatoShibbySpider(Spider):
    name = "tomato"
    allowed_domains = ["tomato.groov.pl"]
    start_urls = ["http://tomato.groov.pl/download"]

    def parse(self, response):
        for link in response.xpath("//table//tr"):
            if not link.xpath("./td[2]/a"):
                continue

            text = link.xpath("./td[2]/a/text()").extract()[0]
            href = link.xpath("./td[2]//@href").extract()[0]

            if ".." in href:
                continue
            elif href.endswith('/'):
                build = response.meta.get("build", None)
                product = response.meta.get("product", None)

                if not product:
                    product = text
                elif not build:
                    build = text.replace("build", "")

                yield Request(
                    url=urlparse.urljoin(response.url, href),
                    headers={"Referer": response.url},
                    meta={"build": build, "product": product},
                    callback=self.parse)
            elif any(href.endswith(x) for x in [".bin", ".elf", ".fdt", ".imx", ".chk", ".trx"]):
                item = FirmcrawlerItem()
                item["productVersion"] = FirmwareLoader.find_version_period(
                    os.path.splitext(text)[0].split("-"))
                item["publishTime"] = FirmwareLoader(date_fmt=["%Y-%m-%d"]).find_date(link.xpath("./td[3]/text()").extract())
                item["productClass"] = "Router"
                item["productModel"] = response.meta["product"]
                item["description"] = ""
                item["url"] = href
                item["firmwareName"] = href.split('/')[-1]
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["manufacturer"] = "tomato"
                yield item
                print "firmware name:", item["firmwareName"]

