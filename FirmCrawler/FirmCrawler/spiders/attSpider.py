# _*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2018.09.08"
__status__ = "ok"


from scrapy.spiders import Spider
from scrapy.http import Request
import scrapy
import time
import urllib2

import FirmCrawler.items as MI
#from firmware.loader import FirmwareLoader

import urlparse

class ATTSpider(Spider):
    name = "att"
    allowed_domains = ["bellsouth.net"]
    start_urls = ["http://cpems.bellsouth.net/firmware"]
    timeout = 10

    def parse(self, response):
        for href in response.xpath("//a/@href").extract():
            if href == ".." or href == "/":

                continue
            elif href.endswith(".bin") or href.endswith(".upg"):
                item = MI.FirmcrawlerItem()
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["manufacturer"] = "att"
                absurl = urlparse.urljoin(response.url,href)
                item["url"] = absurl
                item["firmwareName"] = href

                #invoking the network
                res = ""
                try:
                    res = urllib2.urlopen(urllib2.Request(
                        item["url"], None), timeout=ATTSpider.timeout)
                except Exception, e:
                    print e
                modfile = res.headers["last-modified"]
                try:
                    array = time.strptime(modfile, u"%a, %d %b %Y %H:%M:%S GMT")
                    item["publishTime"] = time.strftime("%Y-%m-%d", array)
                except Exception, e:
                    print e

                item["productModel"] = href.rsplit(".", 1)[0].split("_")[0]

                item["productVersion"] = ""
                item["productClass"] = ""
                item["description"] = ""
                print "firmwarename:",item["firmwareName"]

                yield item


            elif "/" in href:

                yield Request(
                    url=urlparse.urljoin(response.url, href),
                    callback=self.parse)
