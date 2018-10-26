#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2017.03.15"

from scrapy import Spider
from scrapy.http import Request
import time
import FirmCrawler.items as MI
import re
import urlparse

class TrendnetSpider(Spider):
    name = "trendnet"
    allowed_domains = ["trendnet.com"]
    start_urls = ["http://www.trendnet.com/support/"]
    #start_urls = ["http://downloads.trendnet.com/"]

    def parse(self, response):
        for entry in response.xpath("//select[@id='SUBTYPE_ID']/option"):
            if entry.xpath(".//text()"):
                text = entry.xpath(".//text()").extract()[0]
                href = entry.xpath("./@value").extract()[0]

                yield Request(
                    url=urlparse.urljoin(response.url, href),
                    meta={"product": text},
                    headers={"Referer": response.url},
                    callback=self.parse_product)

    def parse_product(self, response):
        for tab in response.xpath("//ul[@class='etabs']//a"):
            text = tab.xpath(".//text()").extract()[0]
            href = tab.xpath("./@href").extract()[0]

            if "downloads" in text.lower():
                yield Request(
                    url=urlparse.urljoin(response.url, href),
                    meta={"product": response.meta["product"]},
                    headers={"Referer": response.url},
                    callback=self.parse_download)

    def parse_download(self, response):
        for entry in response.xpath('//div[@class="downloadtable"]'):
            if entry.xpath('./ul[@class="mainlist" and position() >1]'):
                context = entry.xpath('./ul[@class="mainlist" and position() = 3]')
            else:
                context = entry.xpath('./ul[@class="mainlist" and position() = 1]')

            text = context.xpath(".//text()").extract()

            if "firmware" in " ".join(text).lower():
                #print "download url:",response.url

                publishTime = context.xpath('./li[@class="maindescription" and position() = 2]/text()').extract().pop().strip()
                try:
                    filename = context.xpath('./li[@class="maindescription" and position() = 1]/div//text()').extract().pop().split(': ')[-1]
                except:
                    filename = context.xpath('./div//text()').extract().pop().split(': ')[-1]

                desc = context.xpath('./li[@class="maindescription" and position() = 1]/ol//text()').extract()
                description = str().join(desc).strip()
                text = entry.xpath(".//li[@class='maindescription' and position() = 1]//text()").extract()

                match = re.search("(\(.*\)|[Vv]?(\d\d?\.)+\d\d?|[Vv]\d+)",filename)
                if match:
                    version = match.group().split('(')[-1].split(')')[0]
                else:
                    version = ""

                #url
                #onclick="MM_openBrWindow('/asp/download_manager/inc_downloading.asp?iFile=26386','26386','width=500,height=250,scrollbars=yes,resizable=yes')"
                href = entry.xpath(".//li[@class='maindescription']//a/@onclick").extract()[
                    0].split('\'')[1] + "&button=Continue+with+Download&Continue=yes"
                absurl = urlparse.urljoin(response.url,href)

                item = MI.FirmcrawlerItem()
                item["productModel"] = response.meta["product"]
                item["firmwareName"] = filename
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["manufacturer"] = "trendnet"
                item["description"] = description
                item["productVersion"] = version
                item["url"] = absurl
                #publish time
                item["publishTime"] = ""
                try:
                    array = time.strptime(publishTime, u"%m/%d/%Y")
                    item["publishTime"] = time.strftime("%Y-%m-%d", array)
                except Exception, e:
                    print e

                item["productClass"] = "" #not do

                print "firmwarename:",item["firmwareName"]
                yield item


