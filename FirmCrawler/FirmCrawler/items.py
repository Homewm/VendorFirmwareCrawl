# -*- coding: utf-8 -*-

# 用来定义需要保存的变量，其中的变量用Field来定义，类似于python的字典

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FirmcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    manufacturer = scrapy.Field()
    firmwareName = scrapy.Field()
    description = scrapy.Field()
    publishTime = scrapy.Field()
    productModel = scrapy.Field()   #产品型号
    productVersion = scrapy.Field()
    productClass = scrapy.Field()
    crawlerTime = scrapy.Field()

    '''
    item["productVersion"] = ""
    item["publishTime"] = ""
    item["productClass"] = ""
    item["productModel"] = ""
    item["description"] = ""
    item["url"] = ""
    item["firmwareName"] = ""
    item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
    item["manufacturer"] = ""
    '''

    '''
    suffix = ["bin", "bix", "trx", "img", "dlf", "tfp", "rar", "zip","ipk",
              "bz2","BIN","gz","7z","lzma","tgz","exe","ZIP","tar","ubi",
              "uimage","rtf","ram","elf","ipa","chm","dsw","dsp","clw","mav",
              "dav","upg","bfp","hex","npk"]
    '''
    # "zyxel"
    # "ftp://ftp2.zyxel.com/AMG1001-T10A/"



    #not used
    packedTime = scrapy.Field()
    Title = scrapy.Field()
    Rawlink = scrapy.Field()
    Info = scrapy.Field()
    Status = scrapy.Field()
    need_login = scrapy.Field()
    Release_time = scrapy.Field() #




