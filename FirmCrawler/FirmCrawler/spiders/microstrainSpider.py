# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.9.14"

from scrapy import Spider
from FirmCrawler.items import FirmcrawlerItem
from FirmCrawler.loader import FirmwareLoader
import time
import urllib2


class MicrostrainSpider(Spider):
    name = "microstrain"
    allowed_domains = ["microstrain.com"]
    start_urls = ["http://www.microstrain.com/support"]
    timeout = 12

    # http://files.microstrain.com/8401-0006-Firmware-Upgrades-for-3DM-GX3.pdf

    firmware = ["http://files.microstrain.com/MicroStrain_Wireless_Firmware.zip",
                "http://download.microstrain.com/3DM-GX3-Upgrades/3DM-GX3-15_25_MIP_firmware_upgrade.zip",
                "http://download.microstrain.com/3DM-GX3-Upgrades/3DM-GX3-25_Single_Byte_firmware_upgrade.zip",
                "http://download.microstrain.com/3DM-GX3-Upgrades/3DM-GX3-35_MIP_firmware_upgrade.zip",
                "http://download.microstrain.com/3DM-GX3-Upgrades/3DM-GX3-45_MIP_firmware_upgrade.zip"]

    def parse(self, response):
        for url in self.firmware:
            item = FirmcrawlerItem()
            item["productVersion"] = ""
            item["productModel"] = url.split("/")[-1].split("_")[0]
            item["description"] = ""
            item["productClass"] = ""  # more class
            item["url"] = url
            item["firmwareName"] = url.split("/")[-1]
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["manufacturer"] = "microstrain"
            item["publishTime"] = ""
            yield item
            print "firmwarename:",item["firmwareName"]

