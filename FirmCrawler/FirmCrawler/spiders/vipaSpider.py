#-*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.19"


'''网站页面结构发生改变,代码基本全部重写'''


from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time
from FirmCrawler import *


class VipaSpider(Spider):
    name = "vipa"
    timeout = 20
    trytimes = 3
    start_urls = ["http://www.vipa.com/en/service-support/downloads/firmware"]

    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    headurl = "http://www.vipa.com/"


    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_list)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "vipa"
        yield request


    def parse_list(self, response):
        prototype = response.meta['prototype']

        p_list = response.selector.xpath('//div[@id="c10133"]/p')
        href_list = p_list.xpath('./a/@href').extract()
        # print href_list
        for href in href_list:
            url = urlparse.urljoin(VipaSpider.headurl,href)
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = response.meta["prototype"]
            yield request

    def parse_page(self, response):
        prototype = response.meta['prototype']

        lines = response.selector.xpath('//div[@class="sbfolderdownload"]/div[1]/a')
        div_list = response.selector.xpath('//div[@id="sbfolderFolderWrap"]/div[@class="sbfolderFolder"]')
        href_list = div_list.xpath('./a/@href').extract()
        for href in href_list:
            url = urlparse.urljoin(VipaSpider.headurl, href)

            request = scrapy.Request(url, callback=self.parse_page)
            request.meta["prototype"] = response.meta["prototype"]
            yield request

        for a in lines:
            filename = a.xpath("text()").extract().pop()
            filetype = filename.rsplit(".", 1).pop().strip().lower()
            VipaSpider.allsuffix.add(filetype)

            if not filetype in VipaSpider.typefilter:
                item = MI.FirmcrawlerItem(prototype)
                item["productVersion"]=""
                item["publishTime"]=""
                item["productClass"]=""
                item["productModel"]=""
                item["description"]=""

                url = response.urljoin(a.xpath("@href").extract().pop())
                item["url"]=url.replace(" ","%20")
                item["firmwareName"] = filename
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["description"] = str().join(a.xpath("//div[@class='up']//text()").extract())

                try:
                    res = urllib2.urlopen(urllib2.Request(item["url"], None), timeout=VipaSpider.timeout)
                except Exception,e:
                    print e

                modfile = res.headers["last-modified"]

                try:
                    array = time.strptime(modfile, u"%a, %d %b %Y %H:%M:%S GMT")
                    item["publishTime"] = time.strftime("%Y-%m-%d", array)
                except Exception, e:
                    print e

                #divide version
                try:
                    #ss1 = ["FEE0","3Bxxx"]
                    #ss2 = ["Bb000082","BB000088","BB000090","BB000021"]
                    m = filename.split("_")
                    #针对CPU314SE_V3502.zip
                    likeStand= m[-1].replace(".zip","").replace(".bin","").replace(".BIN","").replace(".os","").replace(".WEC","")
                    # aim at  Px000008_V208_CPU.zip  or  CP 208-1DP01_V522_a2.zip
                    if likeStand in ["DP","CPU","CP","image","a1","a2","a3"]:
                        likeStand = m[-2]
                    if likeStand in ["Tool","CXX"]:
                        likeStand = ""
                    #Special case:
                    if likeStand=="OLD V111 HW V1.0":
                        likeStand = "V1.0"
                    # Special case:
                    if likeStand == "IM208":
                        likeStand = "V419"
                    if likeStand in ["DEMO"]:
                        if filename.split("_")[-2].split("-")[0] in ["ZENON"]:
                            likeStand = filename.split("_")[-2].split("-")[1]
                    #aim at WinCE-5.0_520MHz_PROF-09-01-15_ZENON-6.22-SP0-B6.zip
                    likeStand1 = likeStand.split("-")[0]
                    if likeStand1 in ["M","MOV","ZENON"]:
                        likeStand = likeStand.split("-")[1]
                    if likeStand1 in ["CORE", "PROF"]:
                        likeStand = ""

                    #aim at BB000021.214
                    likeStand2 = likeStand.split(".")[0]
                    if likeStand2 in ["Bb000082","BB000088","BB000090","BB000021","Bb000125"]:
                        likeStand = ""
                    #remove
                    if m[0]=="MicroSD":
                        likeStand = ""
                    item["productVersion"] = likeStand


        #http://www.vipa.com/en/service-support/downloads/firmware/hmi/?tx_sbfolderdownload_pi1[dp]=Panel PC%2F67K-PNJ0-EB&cHash=955c0daa9e29675263d07040444dc23f
                    URL_split1 = item["url"].split("/")[6].replace('%20', " ").strip()
                    URL_split2 = item["url"].split("/")[7].replace('%20', " ").strip()


                    item["productModel"] = URL_split1 + "/" + URL_split2


                    if URL_split1 == "updater":
                        item["productClass"] = "Miscellaneous & Accessoiries"
                    elif URL_split1 == "Components":
                        item["productClass"] = "Miscellaneous & Accessoiries"

                    elif URL_split1 == "Controls":
                        item["productClass"] = "Control Systems"

                    elif URL_split1 == "HMI":
                        item["productClass"] = "HMI"

                    else:
                        item["productClass"] = ""

                    # item["productModel"] = item["url"].split("/")[6].replace('%20', " ").strip()
                    #
                    #
                    # if item["productModel"] == "updater":
                    #     item["productClass"] = "Miscellaneous & Accessoiries"
                    # elif item["productModel"] == "Components":
                    #     item["productClass"] = "Miscellaneous & Accessoiries"
                    #
                    # elif item["productModel"] == "Controls":
                    #     item["productClass"] = "Control Systems"
                    #
                    # elif item["productModel"] == "HMI":
                    #     item["productClass"] = "HMI"
                    #
                    # else:
                    #     item["productClass"] = ""
                except:
                    pass

                # print "version:", item["productVersion"]
                # print item["url"]
                print "firmwarename:", item["firmwareName"]
                # print "productModel:", item["productModel"]
                # print "productClass:", item["productClass"]
                yield item

