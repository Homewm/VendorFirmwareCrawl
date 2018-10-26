# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.03.25"

from scrapy import Spider
from scrapy.http import Request
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import json
import urlparse
import time


class UbiquitiSpider(Spider):
    name = "ubiquiti"
    allowed_domains = ["ubnt.com"]
    start_urls = ["http://www.ubnt.com/download/"]

    def parse(self, response):
        for platform in response.xpath(
                "//a[@data-ga-category='download-nav']/@data-slug").extract():
            yield Request(
                url=urlparse.urljoin(response.url, "?group=%s" % (platform)),
                headers={"Referer": response.url,
                         "X-Requested-With": "XMLHttpRequest"},
                callback=self.parse_json)

    def parse_json(self, response):
        json_response = json.loads(response.body_as_unicode())

        if "products" in json_response:
            for product in json_response["products"]:
                yield Request(
                    url=urlparse.urljoin(
                        response.url, "?product=%s" % (product["slug"])),
                    headers={"Referer": response.url,
                             "X-Requested-With": "XMLHttpRequest"},
                    meta={"product": product["slug"]},
                    callback=self.parse_json)

        if "url" in response.meta:
            item = FirmcrawlerItem()
            item["productVersion"] = response.meta["version"]
            item["publishTime"] = response.meta["date"]
            item["productClass"] = ""
            item["productModel"] = response.meta["product"]
            item["description"] = response.meta["description"]
            item["url"] = response.meta["url"]
            item["firmwareName"] = item["url"].split('/')[-1]
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["manufacturer"] = "ubiquiti"
            # print "url:",response.meta["url"]
            yield item
            print "firmwarename:",item["firmwareName"]

        elif "product" in response.meta:
            for entry in json_response["downloads"]:
                if entry["category__slug"] == "firmware":

                    if entry["sdk__id"]:
                        yield Request(
                            url=urlparse.urljoin(
                                response.url, "?gpl=%s&eula=True" % (entry["sdk__id"])),
                            headers={"Referer": response.url,
                                     "X-Requested-With": "XMLHttpRequest"},
                            meta={"product": response.meta["product"], "date": entry["date_published"], "build": entry[
                                "build"], "url": entry["file_path"], "version": entry["version"], "description": entry["name"]},
                            callback=self.parse_json)
                    else:
                        # print "url:",entry["file_path"]
                        item = FirmcrawlerItem()
                        item["productVersion"] = entry["version"]
                        item["publishTime"] = entry["date_published"]
                        item["productClass"] = ""
                        item["productModel"] = response.meta["product"]
                        item["description"] = entry["name"]
                        item["url"] = entry["file_path"]
                        item["firmwareName"] = item["url"].split('/')[-1]
                        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        item["manufacturer"] = "ubiquiti"
                        yield item
                        print "firmwarename:", item["firmwareName"]
