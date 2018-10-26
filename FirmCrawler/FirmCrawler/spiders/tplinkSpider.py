#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2018.09.18"



'''
    (I)网站结构发生全面的变化,代码基本全部重写
    (II)未解决的问题:
        1.同样的固件名或者发行时间结构,不清楚为什么有的获取不到;
        2.针对爬取,有的时候能爬取到信息,有的时候爬取不到.
        针对上面两个问题,暂时没有找到解决的办法,猜测是反爬虫机制的设置.

'''

from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import urlparse
import re


class TplinkSpider(Spider):
    name = "tplink"
    allowed_domain = ["tp-link.com.cn"]

    #"http://service.tp-link.com.cn/list_download_software_1_0.html",  ###这个网址也能用
    start_urls = [
        "http://service.tp-link.com.cn/download?classtip=software&p=1&o=0"
    ]
    headurl = "http://service.tp-link.com.cn/"

    # must be lower character
    suffix = ["bin", "bix", "trx", "img", "dlf", "tfp", "rar", "zip","ipk","bz2","BIN","gz","7z","lzma","tgz","exe","ZIP","tar","ubi","uimage","rtf","ram","elf","ipa","chm","dsw","dsp","clw","mav","dav","DAV","Dav","iso"]
    allsuffix = Set()
    timeout = 8
    trytimes = 3
    # classify seek model web page http://www.tp-link.com.cn/search.html?keywords=TL-IPC&x=0&y=0
    router = ["TL-WR", "TL-R1", "TD-W8", "TL-MR", "TL-WV", "TL-WD", "TL-ER", "TL-TR", "TL-H2", "TL-CP", "TL-PW",
              "TL-H3", "TL-H6", "TL-R4", "TL-H1"]
    modem = ["TD-89", "TD-86", "TD-88", "TD-87", "TL-GP", "TL-EP"]
    camera = ["TL-SC", "TL-IP", "TL-NV"]
    switch = ["TL-SG", "TL-SL"]
    ap = ["TL-WA", "TL-AC", "TL-AP"]
    printing_server = ["TL-PS"]
    NetworkTVBox = ["TP"]


    def parse(self, response):
        for page in xrange(1,138): #total page is 137
            # url = "http://service.tp-link.com.cn/list_download_software_" + str(page) + "_0.html"   ###这个网址也能用
            url = "http://service.tp-link.com.cn/download?classtip=software&p=" + str(page)+"&o=0"
            request = scrapy.Request(url, callback=self.parse_list)
            yield request


    def parse_list(self,response):

        tr_list = response.xpath('//div[@class="main"]/section[2]/section[2]/div/div/table/tbody/tr')
        for tr in tr_list:
            href = tr.xpath('.//th[1]/a/@href').extract()[0]
            url = urlparse.urljoin(TplinkSpider.headurl, href)
            # print url

            request = scrapy.Request(url, callback=self.parse_page)
            yield request

    def parse_page(self,response):
        file_name = response.selector.xpath('//div[@class="content"]/table/tbody/tr[1]/td[2]/text()').extract()
        if file_name:
            filename = file_name[0]

            #version
            c = re.search(r'[V|v][0-9]+.[0-9]', filename)  # c maybe not exist
            if c :
                c = c.group()
                if c[-2] == "_":  # TL-WR700N_V1_V2_130415.rar    scrapy V2_1 use V2
                    cc = c.split("_")
                    version = cc[0]
                else:
                    version = c

            #model
            m = filename.split(" ") #TL-TR862 V1.0_TL-TR861 5200L V1.0_130815标准版
            productModel = m[0].split("_", 1)[0]
            if productModel == "企业级路由器应用数据库文件V1.1.9":
                productModel = ""

            #classify
            pattern = re.compile(r"T(L|D)-..")
            classraw = pattern.match(productModel)
            if classraw:
                category = classraw.group()
                if category in TplinkSpider.router:
                    productClass = "Router"
                elif category in TplinkSpider.switch:
                    productClass = "Switch"
                elif category in TplinkSpider.camera:
                    productClass = "Camera"
                elif category in TplinkSpider.modem:
                    productClass = "Modem"
                elif category in TplinkSpider.ap:
                    productClass = "Ap"
                elif category in TplinkSpider.printing_server:
                    productClass = "Printing_server"
                else:
                    productClass = ""

            else:
                if productModel in TplinkSpider.NetworkTVBox:
                    productClass = "NetworkTVBox"
                elif productModel == "TG1":
                    productClass = "Router"
                else:
                    productClass = ""

        else:
            filename = ""
            version = ""
            productClass = ""
            productModel = ""
        # print filename
        # print version
        # print productModel
        # print productClass

        publish_Time = response.xpath('//div[@class="content"]/table/tbody/tr[3]/td[2]/text()').extract()
        if publish_Time:
            publishTime = publish_Time[0]
        else:
            publishTime = ""

        abs_url = response.xpath('//div[@class="content"]/table/tbody/tr[4]/td[2]/a/@href').extract()
        if abs_url:
            absurl = abs_url[0]
        else:
            absurl = ""

        describle = response.xpath('//div[@class="content"]/table/tbody/tr[5]/td[2]/text()').extract()
        if describle:
            desc = " ".join(describle).strip()
        else:
            desc = ""

        item = MI.FirmcrawlerItem()
        item["productVersion"] = version
        item["publishTime"] = publishTime
        item["productClass"] = productClass
        item["productModel"] = productModel
        item["description"] = desc
        item["url"] = absurl
        item["firmwareName"] = filename
        item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        item["manufacturer"] = "tplink"
        yield item
        print "firmwarename:", item["firmwareName"]

        return





    # def parse_page(self,response):
    #     itemurl = response.selector.xpath('//div[@class="download"]//tr[5]/td[2]/a/@href').extract().pop()
    #     absurl = urlparse.urljoin(response.url,itemurl)
    #     filetype = absurl.rsplit(".",1).pop().strip().lower()
    #     TplinkSpider.allsuffix.add(filetype)
    #     if filetype in TplinkSpider.suffix:
    #         prototype = response.meta['prototype']
    #         item = MI.FirmcrawlerItem(prototype)
    #         item["firmwareName"] = absurl.rsplit("/",1).pop()
    #         item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
    #         item["url"] = absurl
    #         modifiedTime = response.selector.xpath('//div[@class="download"]//tr[4]/td[2]/text()').extract().pop()
    #         try:
    #             array = time.strptime(modifiedTime, u"%Y/%m/%d")
    #             item["publishTime"] = time.strftime("%Y-%m-%d", array)
    #         except Exception, e:
    #             print e
    #
    #         des = response.selector.xpath('//div[@class="download"]//tr[6]/td[2]//text()').extract()  #the last "//" aim to locate the different path
    #         item["description"]  = str().join(des)
    #         softname = response.selector.xpath('//div[@class="download"]//tr[1]/td[2]/text()').extract().pop()
    #         #version
    #         c = re.search(r'[V|v][0-9]+.[0-9]', softname)  # c maybe not exist
    #         if c :
    #             c = c.group()
    #             if c[-2] == "_":  # TL-WR700N_V1_V2_130415.rar    scrapy V2_1 use V2
    #                 cc = c.split("_")
    #                 item['productVersion'] = cc[0]
    #             else:
    #                 item['productVersion'] = c
    #         else:
    #             item['productVersion'] = ""
    #
    #         #model
    #         m = softname.split(" ") #TL-TR862 V1.0_TL-TR861 5200L V1.0_130815标准版
    #         item['productModel'] = m[0].split("_", 1)[0]
    #         if item['productModel'] == "企业级路由器应用数据库文件V1.1.9":
    #             item['productModel'] = ""
    #
    #         #classify
    #         pattern = re.compile(r"T(L|D)-..")
    #         classraw = pattern.match(item['productModel'])
    #         if classraw:
    #             category = classraw.group()
    #             if category in TplinkSpider.router:
    #                 item["productClass"] = "Router"
    #             elif category in TplinkSpider.switch:
    #                 item["productClass"] = "Switch"
    #             elif category in TplinkSpider.camera:
    #                 item["productClass"] = "Camera"
    #             elif category in TplinkSpider.modem:
    #                 item["productClass"] = "Modem"
    #             elif category in TplinkSpider.ap:
    #                 item["productClass"] = "Ap"
    #             elif category in TplinkSpider.printing_server:
    #                 item["productClass"] = "Printing_server"
    #             else:
    #                 item["productClass"] = ""
    #
    #         else:
    #             if item['productModel'] in TplinkSpider.NetworkTVBox:
    #                 item["productClass"] = "NetworkTVBox"
    #             elif item['productModel'] == "TG1":
    #                 item["productClass"] = "Router"
    #             else:
    #                 item["productClass"] = ""
    #         yield item
    #         print "firmwarename:",item["firmwareName"]
    #     return











