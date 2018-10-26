# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.10"

"""修改后正常使用,原因在于地址发生改变,固件存放的文件地址发生了改变.修改后正常使用."""

from sets import Set
from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
import re
import urlparse
import urllib2
import time

# directory and file don't have a clear feature , more level , stastic

class hikvisionSpider(Spider):
    name = "hikvision"
    timeout = 20
    trytimes = 3
    start_urls = ["http://www.hikvisioneurope.com/portal/?dir=portal/Product Firmware 2018"]
    # must be lower character
    allsuffix = Set()
    suffix = ["bin", "bix", "trx", "img", "dlf", "tfp", "rar", "zip","ipk","bz2","BIN","gz","7z","lzma","tgz","exe","ZIP","tar","ubi","uimage","rtf","ram","elf","ipa","chm","dsw","dsp","clw","mav","dav","DAV","Dav","iso"]


    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        request.meta["prototype"] = MI.FirmcrawlerItem()
        request.meta["prototype"]["manufacturer"] = "hikvision"
        yield request

    def parse_page(self, response):
        lists = response.selector.xpath('//table[@id="datatable-checkbox"]/tbody/tr[position()>1]')
        prototype = response.meta['prototype']

        for i in lists:
            listsdownbutton = i.xpath('./td[4]/a/@href').extract() #file but not directory

            if not listsdownbutton: # it is directory
                dirurl = i.xpath('./td[1]/a[1]/@href').extract()
                absurl = urlparse.urljoin(response.url, dirurl[0])
                request = scrapy.Request(absurl, callback=self.parse_page)
                request.meta["prototype"] = response.meta["prototype"]
                yield request
            else:
                #get information
                absurlfile = urlparse.urljoin(response.url,listsdownbutton[0])
                filename = absurlfile.rsplit('/',1)[-1]
                filename = urllib2.unquote(filename) #unquoto mean end quote,and decode
                filetype = filename.split('.')[-1]
                publishtime = i.xpath('./td[3]/text()').extract()[0]
                hikvisionSpider.allsuffix.add(filetype)

                if filetype in hikvisionSpider.suffix:
                    # print "zhua qu"
                    item = MI.FirmcrawlerItem(prototype)
                    item["firmwareName"] = filename
                    item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    item["url"] = absurlfile
                    item["publishTime"] = publishtime
                    item["description"] = absurlfile.split('/')[5] + "/" + absurlfile.split('/')[6]
                    item["productVersion"] = ""
                    item["productModel"] = ""
                    item["productClass"] = ""  #waiting for doing it

                    #version
                    regVersion = re.compile(r'[V,v]*[0-9]\.[0-9][0-9]*\.*[0-9]*[0-9]*')
                    regVersions = regVersion.search(filename)
                    if regVersions:  # 当固件名中版本号存在时，型号一定存在
                        item["productVersion"] = regVersions.group()

                        #-----productModel-------
                        Modeldiv1 = filename.split("_")
                        Modeldiv1len = len(Modeldiv1)
                        if filename.split(" ")[
                            0] == "Baseline":  # 匹配Baseline开头的固件Baseline IPD_Raptor_En_5.2.8_150124.zip
                            # baseline四种情况：
                            if len(filename.split(" ")) >= 4:  # 匹配　Baseline%20Firmware_IPC_R4%20series_En_V5.2.0%20140721.zip
                                item["productModel"] = filename.split(" ", 2)[1]
                            elif len(filename.split(" ")) == 2:  # 匹配Baseline%20IPD_Raptor_En_5.3.0_150410.zip和Baseline_IPD_En_V3.2.0%20131223%28Released%29.zip
                                if regVersion.search(filename.split(" ")[1]):
                                    Modeldiv021 = filename.split(" ")[1].split("_", 2)
                                    arr = []
                                    arr.append(Modeldiv021[0])
                                    arr.append(Modeldiv021[1])
                                    item["productModel"] = "_".join(arr)
                                else:
                                    Modeldiv022 = filename.split(" ")[1].split("_", 2)
                                    arr = []
                                    arr.append(Modeldiv022[0])
                                    arr.append(Modeldiv022[1])
                                    item["productModel"] = "_".join(arr)
                            elif len(filename.split(" ")) == 3:  # 匹配Baseline%20IPC_R1_En_V5.2.0%20140721.zip

                                Modeldiv03 = filename.split(" ", 2)[1].split("_", 2)
                                arr = []
                                arr.append(Modeldiv03[0])
                                arr.append(Modeldiv03[1])
                                item["productModel"] = "_".join(arr)

                        elif re.compile(r"[D,d]igicap").search(filename):  # digicap_STD_V3.1.2_20140512.zip
                            item["productModel"] = "Digicap"
                        elif Modeldiv1len > 1 and regVersion.search(Modeldiv1[1]):  # DS-6400HDI-T_V1.5.0 build 120601.rar.zip
                            item["productModel"] = Modeldiv1[0]

                        else:  # 普通情况，取前两位　NVR_71_4_8_SN_BL_EN_STD_V3.0.18_151231.zip
                            # Modeldiv1= firewName.split("_")　#放到条件语句前定义
                            # 主要处理型号中多位数字这种情况　DS-71_72_73_81_80_9000HQHI(HGHI)-SH_ML_STD_V3.1.3_150212.zip
                            arr1 = []
                            count = 1  # 统计匹配到数字的位数
                            flags = False
                            for element in Modeldiv1:

                                if count < 3:
                                    if re.compile(r"\(").search(element):  # 针对这种情况：NVR_%2871_16_SN%29BL_ML_Eurpon_South_STD_V3.0.17_150804.zip　　　　NVR_(71
                                        flags = True
                                    if re.compile(r"\)").search(element):  # 针对这种情况：NVR_%2871_16_SN%29BL_ML_Eurpon_South_STD_V3.0.17_150804.zip　　　　NVR_(71
                                        flags = False
                                    arr1.append(element)
                                    count += 1
                                else:
                                    if regVersion.search(element):
                                        break
                                    if re.compile(r"^[0-9]\w*").search(element) or flags == True:
                                        arr1.append(element)
                                        count += 1
                                        if re.compile(r"\)").search(element):
                                            flags = False
                                    else:
                                        break

                            item["productModel"] = "_".join(arr1)
                        #-----productModel-------
                    else:
                        item["productVersion"] = ""
                        item["productModel"] = ""
                    print "firmwareName:", item["firmwareName"]
                    yield item
        #print "all suffix:",hikvisionSpider.allsuffix
        return















