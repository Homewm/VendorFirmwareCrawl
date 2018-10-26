# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2017.02.24"
from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import time

class OpenwrtSpider(Spider):
    name = "openwrt"
    allowed_domains = ["openwrt.org.cn"]
    start_urls = [
        "http://downloads.openwrt.org.cn/OpenWrt-DreamBox/",
        "http://downloads.openwrt.org.cn/PandoraBox/",
        "http://downloads.openwrt.org.cn/openwrtcn_img/",
        "http://downloads.openwrt.org.cn/ar_series_img/",
        "http://downloads.openwrt.org.cn/zjhzzyf_img/",
    ]
    # must be lower character
    suffix = ["bin", "bix", "trx", "img", "dlf", "tfp", "rar", "zip","ipk","bz2","BIN","gz","7z","lzma","tgz","exe","ZIP","tar","ubi","uimage","rtf","ram","elf","ipa","chm","dsw","dsp","clw","mav","dav","DAV","Dav","iso"]
    allsuffix = Set()
    timeout = 8
    trytimes = 3

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "openwrt"
        yield request

    def parse_page(self, response):
        r = response.selector.xpath("//pre").re("<a[ ]*href=\"(.*)\".*>.*</a>[ ]*(.*:.*)\r\n")  # [0-9]{2}
        i = 0
        prototype = response.meta['prototype']
        while i < len(r):
            if r[i][-1] == "/":
                request = scrapy.Request(
                    response.url + r[i], callback=self.parse_page)
                request.meta["prototype"] = response.meta["prototype"]
                yield request
            elif r[i].rsplit(".").pop().lower() in OpenwrtSpider.suffix:
                item = MI.FirmcrawlerItem(prototype)
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["firmwareName"] = r[i]
                item["url"] = response.url + r[i]
                item["productModel"] =""
                #divided model
                firmWareName=item["firmwareName"]

                divName1=firmWareName.split("-")
                try:
                    #aim at PandoraBox-realtek-rtl8198c-alpha-fw.bin
                    if divName1[0]=="PandoraBox":
                        likeModel=divName1[1]+"-"+divName1[2]
                    elif divName1[0]=="openwrt":
                        likeModel=divName1[1]
                    elif divName1[1]=="openwrt":
                        likeModel = divName1[2]
                    else:
                        likeModel=""
                    item["productModel"]=likeModel
                except:
                    pass
                #The full firmware of openwrt are Router!
                item["productClass"] = "Router"

                try:
                    p_s = r[i + 1].split(" ")
                    item["publishTime"] = p_s[0]
                    a = item["publishTime"]
                    a = a.strip()
                    try:
                        array=time.strptime(a,u"%d-%b-%Y")
                        item["publishTime"] = time.strftime("%Y-%m-%d",array)
                    except Exception, e:
                        print e
                except Exception,e:
                    print e


                yield item
                print "firmwareName:",item["firmwareName"]
            else:
                OpenwrtSpider.allsuffix.add(r[i].rsplit(".").pop().lower())
            i += 2
        #print "all suffix:",OpenwrtSpider.allsuffix
        return
