# -*- coding: UTF-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.17"

from sets import Set
from scrapy.spiders import Spider
import scrapy
import re
import urlparse
import FirmCrawler.items as MI
import urllib2
import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class miwifiSpider(Spider):
    name = "miwifi"
    timeout = 12
    trytimes = 3
    start_urls = [
        "http://miwifi.com/miwifi_download.html"
    ]
    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()
    def parse(self, response):
        browser = webdriver.PhantomJS(executable_path="/root/zgd/code/FirmCrawler/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
        browser.implicitly_wait(miwifiSpider.timeout)
        browser.set_page_load_timeout(miwifiSpider.timeout)
        try:
            browser.get(response.url)
        except TimeoutException:
            print "url not parse???"
            pass

        WebDriverWait(browser, miwifiSpider.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "dl_bodying")))

        items = browser.find_elements_by_xpath('//div[@class="dl_bodying"]/ul/li[2]/div')
        for item in items:
            absurl = item.find_element_by_class_name("link_download").get_attribute('href')
            if absurl: #hava same url not show in website
                firmname = absurl.split("/")[-1]
                divide = firmname.rsplit(".",1)[0].split("_")
                if divide[-1] == "ENG":
                    version = divide[-2]
                    model = divide[1]
                else:
                    version = divide[-1]
                    if divide[1] == "all":
                        model = divide[0]
                    else:
                        model = divide[1]
                item = MI.FirmcrawlerItem()
                item["productVersion"] = version
                item["productClass"] = "Router"
                item["productModel"] = model
                item["description"] = ""
                item["url"] = absurl
                item["firmwareName"] = firmname
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["manufacturer"] = "miwifi"
                item["publishTime"] = ""
                yield item
                print "firmware name:", item["firmwareName"]




