#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2017.03.03"

from scrapy import Spider
from scrapy.http import Request
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import json
import urlparse
import time


class DLinkSpider(Spider):
    name = "dlink"
    allowed_domains = ["dlink.com"]
    start_urls = ["http://support.dlink.com/AllPro.aspx"]

    custom_settings = {"CONCURRENT_REQUESTS": 3}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ServiceTypecookies': "ServiceType=2&ServiceTypeshow=1"}, dont_filter=True)

    def parse(self, response):
        for entry in response.xpath("//tr/td[1]/a/@alt").extract():
            yield Request(
                url=urlparse.urljoin(
                    response.url, "ProductInfo.aspx?m=%s" % entry),
                headers={"Referer": response.url},
                meta={"product": entry},
                callback=self.parse_product)

    def parse_product(self, response):
        for entry in response.xpath("//select[@id='ddlHardWare']/option"):
            rev = entry.xpath(".//text()").extract()[0]
            val = entry.xpath("./@value").extract()[0]

            if val:
                yield Request(
                    url=urlparse.urljoin(
                        response.url, "/ajax/ajax.ashx?action=productfile&ver=%s" % val),
                    headers={"Referer": response.url,"X-Requested-With": "XMLHttpRequest"},
                    meta={"product": response.meta["product"], "revision": rev},
                    callback=self.parse_json)

    def parse_json(self, response):
        mib = None
        json_response = json.loads(response.body_as_unicode())

        for entry in reversed(json_response["item"]):
            for file in reversed(entry["file"]):
                if file["filetypename"].lower() == "firmware" or file["isFirmF"] == "1":
                    item = FirmcrawlerItem()
                    # print "file url:",file["url"]
                    item["manufacturer"] = "dlink"
                    item["firmwareName"] = file["url"].split('/')[-1]
                    item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    item["url"] = file["url"]
                    item["description"] = file["name"]
                    item["productClass"] = ""
                    item["publishTime"] = file["date"]
                    item["productVersion"] = FirmwareLoader.find_version_period([file["name"]])
                    item["productModel"] = response.meta["product"]
                    yield item

                    print "firmwarename:", item["firmwareName"]
                    # item.add_value("version",
                    #                FirmwareLoader.find_version_period([file["name"]]))
                    # item.add_value("date", file["date"])
                    # item.add_value("description", file["name"])
                    # item.add_value("url", file["url"])
                    # item.add_value("build", response.meta["revision"])
                    # item.add_value("product", response.meta["product"])

                    # yield item.load_item()

