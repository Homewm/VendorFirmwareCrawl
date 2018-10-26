# -*- coding:utf-8 -*-
__author__ = "zhangguodong"
__time__ = "2018.09.17"

'''代码全部重写,网站结构发生改变'''

from scrapy import Spider
import time
import FirmCrawler.items as MI
import scrapy
import urllib, urllib2, urlparse
from sets import Set


class NetgearSpider(Spider):
    name = "netgear"
    timeout = 20
    trytimes = 3
    allowed_domains = ["netgear.cn"]
    start_urls = ["http://support.netgear.cn/download.asp"]

    # must be lower character
    typefilter = ["txt", "pdf"]
    allsuffix = Set()

    headurl = "http://support.netgear.cn"


    def parse(self, response):
        option_list = response.xpath('//div[@id="contenthome"]/div/div[2]/div[3]/table/tr/td/form/div/select/option')
        for option in option_list:
            href_value = option.xpath('./@value').extract()[0]
            if href_value:
                url = urlparse.urljoin(response.url, href_value)
                # print url

                #http://support.netgear.cn/doucument/Detail.asp?id=2328
                #http://support.netgear.cn/doucument/More.asp?id=2329
                ###针对网页上的"获取更多",进行替换
                url_more = url.replace('Detail','More')
                request = scrapy.Request(url_more, callback=self.parse_page)
                yield request

        # url = "http://support.netgear.cn/doucument/More.asp?id=2329"
        # request = scrapy.Request(url, callback=self.parse_page)
        #
        # request.meta["prototype"] = MI.FirmcrawlerItem()
        # request.meta["prototype"]["manufacturer"] = "netgear"
        # yield request


    def parse_page(self, response):
        productModel = response.xpath('.//div[@id="content"]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/div/div[1]/text()').extract()[0]
        # print productModel
        desc = response.xpath('.//div[@id="content"]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/div/div[2]/text()').extract()[0]

        #.//*[@id='content']/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/a
        tr_list = response.xpath('//div[@id="content"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tr[2]/td/table/tr')
        for tr_info in tr_list:
            href = tr_info.xpath('./td[2]/a/@href').extract()[0]
            # print href

            filename = href.split("/")[-1]
            # print filename

            absurl = urlparse.urljoin(NetgearSpider.headurl, href)

            productVersion = tr_info.xpath('./td[2]/a/text()').extract()[0]

            publishTime = tr_info.xpath('./td[3]/text()').extract()
            if publishTime:
                publishTime = publishTime[0].strip()
            else:
                publishTime = ""
            # print publishTime


            item = MI.FirmcrawlerItem()
            item["firmwareName"] = filename
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["url"] = absurl
            item["description"] = desc
            item["productClass"] = ""
            item["productVersion"] = productVersion
            item["productModel"] = productModel
            item["manufacturer"] = "netgear"
            print "firmwarename:", item["firmwareName"]
            yield item



