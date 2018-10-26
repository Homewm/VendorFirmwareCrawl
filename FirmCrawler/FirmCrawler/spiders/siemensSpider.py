#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2019.09.18"


from scrapy.spiders import Spider
import scrapy
import FirmCrawler.items as MI
from sets import Set
import time
import re
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urlparse
# two level ,standard

class siemensSpider(Spider):
    name = "siemens"
    allowed_domain = ["industry.siemens.com"]
    start_urls = [
        "https://support.industry.siemens.com/cs/search?ps=100&search=%E5%9B%BA%E4%BB%B6&type=Download&lc=zh-CN",
        "https://support.industry.siemens.com/cs/search?ps=100&p=1&search=%E5%9B%BA%E4%BB%B6&type=Download&lc=zh-CN",
        "https://support.industry.siemens.com/cs/search?ps=100&p=2&search=%E5%9B%BA%E4%BB%B6&type=Download&lc=zh-CN",
        "https://support.industry.siemens.com/cs/search?ps=100&p=3&search=%E5%9B%BA%E4%BB%B6&type=Download&lc=zh-CN"
    ]


    # must be lower character
    suffix = ["bin", "bix", "trx", "img", "dlf", "tfp", "rar", "zip","ipk","bz2","BIN","gz","7z","lzma","tgz","exe","ZIP","tar","ubi","uimage","rtf","ram","elf","ipa","chm","dsw","dsp","clw","mav","dav"]
    allsuffix = Set()
    timeout = 15
    trytimes = 3
    #product module
    flag1 = ["Classic", "Download", "HotFix", "PNGSD", "Profil", "GSDML", "QuickPatch", "SIMOTION",
             "SINAMICS", "SITRANS", "TIA", "tia"]
    flag2 = ["SSP", "33119786"]
    flag3 = ["HF1", "HF2"]
    flag4 = ["HSP"]
    flagk = ["DOC", "Doc", "1SI", "BFCT", "CFC", "Data-Highway", "EDD", "Firmware", "GSD",
             "L-Version020401", "NC",
             "OP", "RSETUP", "SCOUT", "SIMATIC", "Setup", "SSP-SINAMICS-DCM-V1-3-HF1", "TS",
             "TSA-IE-FW", "TSAIE",
             "TSAIEADVANCED", "UPD", "USB", "Vol", "WinAC", "WinCC", "edd", "patch", "iMap",
             "migrationGSDML", "simotion", "step7", "PC", "Portal",
             "gsdml", "gsdml-v2", "APACS", "FWSP", "HF3", "SCOUT", "V4", "portal"]
    #product class
    Plc = ["PLC", "SIMATIC", "Advanced"]
    Simotion = ["SIMOTION"]
    Sinamics = ["SINAMICS"]
    Sitop = ["SITOP"]
    Mass_flowmeter = ["SITRANS"]
    Et = ["Systeme", "ET", "ET200", ]
    Weighing_module = ["Weighing"]
    Industrial_ethernet = ["2", "3"]
    Industrial_communication = ["Communication"]
    Vfd = ["G"]  # Variable-frequency Drive
    Hmi = ["HMI"]

    def parse(self, response):
        browser = webdriver.PhantomJS(executable_path="/root/zgd/code/FirmCrawler/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
        browser.implicitly_wait(siemensSpider.timeout)
        browser.set_page_load_timeout(siemensSpider.timeout)
        nbrowser = webdriver.PhantomJS(executable_path="/root/zgd/code/FirmCrawler/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
        nbrowser.implicitly_wait(siemensSpider.timeout)
        nbrowser.set_page_load_timeout(siemensSpider.timeout)
        try:
            browser.get(response.url)
        except TimeoutException:
            pass

        WebDriverWait(browser, siemensSpider.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "globalsearch")))

        items = browser.find_elements_by_xpath('//div[@data-bind="compose: $data"]/div/div[2]/span[@data-part="titlePart"]/a')
        # print "item len!! :",len(items)
        for i in items:
            pageurl = i.get_attribute('href')
            yield self.parse_page(pageurl, nbrowser)

    def parse_page(self,url,browser):
        try:
            browser.get(url)
        except TimeoutException:
            pass
        try:
            WebDriverWait(browser, siemensSpider.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "hgroup")))
        except:
            return
        publishtime = browser.find_elements_by_xpath('//div[@class="hgroup"]/hgroup/div/span')
        publishtime = publishtime[-1].text
        try:
            array = time.strptime(publishtime, u"%Y年%m月%d日")
            publishtime = time.strftime("%Y-%m-%d", array)
        except Exception, e:
            print e
            publishtime = ""


        description = browser.find_element_by_xpath('//div[@class="hgroup"]/hgroup/h1').text

        lines = browser.find_elements_by_xpath('//a[@data-file-download=""]')
        #文献属于产品树图文件夹
        firmclass = ""
        try:
            firmdir = browser.find_element_by_xpath(
            """//a[@data-bind="foreach: { data: allPNodes.titles, as: 'title' }, attr: { href: allPNodes.link }"]""").text
            firmclass = firmdir.split(' ')[5]
        except:
            pass

        # product class
        productClass = ""
        if firmclass:
            if firmclass in siemensSpider.Plc:
                productClass = "Plc"
            elif firmclass in siemensSpider.Simotion:
                productClass = "Simotion"
            elif firmclass in siemensSpider.Sinamics:
                productClass = "Sinamics"
            elif firmclass in siemensSpider.Sitop:
                productClass = "Sitop"
            elif firmclass in siemensSpider.Mass_flowmeter:
                productClass = "Mass_flowmeter"
            elif firmclass in siemensSpider.Et:
                productClass = "Et"
            elif firmclass in siemensSpider.Weighing_module:
                productClass = "Weighing_module"
            elif firmclass in siemensSpider.Industrial_ethernet:
                productClass = "Industrial_ethernet"
            elif firmclass in siemensSpider.Industrial_communication:
                productClass = "Industrial_communication"
            elif firmclass in siemensSpider.Vfd:
                productClass = "Vfd"
            elif firmclass in siemensSpider.Hmi:
                productClass = "Hmi"
            else:
                productClass = ""

        for line in lines:
            firmurl = line.get_attribute("href")
            absfirmurl = urlparse.urljoin(url,firmurl)
            filename = absfirmurl.rsplit('/',1)[-1]
            filenameNtype = filename.rsplit('.',1)[0]
            #print "filenameNtype:",filenameNtype
            filetype = filename.split('.')[-1]
            siemensSpider.allsuffix.add(filetype)

            if filetype in siemensSpider.suffix:
                #print "zhua qu"
                item = MI.FirmcrawlerItem()
                item["manufacturer"] = "siemens"
                item["firmwareName"] = filename
                item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = absfirmurl
                item["publishTime"] = publishtime
                item["description"] = description
                item["productClass"] = productClass

                #product module
                item["productModel"] = ""
                name1 = filenameNtype.split('_')[0]  # D4xx_V04_01_02_00_PN21_DP.zip  Classic_1555AA00_V200.EXE
                try:
                    if name1 in siemensSpider.flag1:
                        item["productModel"] = filenameNtype.split("_")[1]
                    elif name1 in siemensSpider.flag2:
                        item["productModel"] = filenameNtype.split("_")[2]
                    elif name1 in siemensSpider.flag3:
                        item["productModel"] = filenameNtype.split("_")[3]
                    elif name1 in siemensSpider.flag4:
                        item["productModel"] = filenameNtype.split("_")[4]
                    elif name1 in siemensSpider.flagk:
                        item["productModel"] = ""
                except:
                    pass
                if item["productModel"] in siemensSpider.flagk:
                    item["productModel"] = ""

                #version
                # regVersion = re.compile(r"(V|v)[0-9]+\_*[0-9]*\_*[0-9]*")
                # regVersion = re.compile(r'(V|v)[0-9].*[0-9]')
                # regVersion = re.compile(r'(V|v)[0-9](.+?)[0-9]', re.IGNORECASE)
                # regVersions = re.match(regVersion, filename)

                regVersions = re.search(r'(V|v)[0-9].*[0-9]', filename)
                if regVersions:
                    item["productVersion"] = regVersions.group()
                else:
                    item["productVersion"] = ""

                #print "item",item

                print "firmwarename:",item["firmwareName"]
                return item
