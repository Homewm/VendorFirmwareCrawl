#_*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2018.09.18"


'''网站结构发生全部变化,代码全部重写'''


from scrapy import Spider
from scrapy.http import Request
import FirmCrawler.items as MI
import time
import re
import urlparse


class UbloxSpider(Spider):
    name = "ublox"
    allowed_domains = ["u-blox.com"]
    start_urls = [
        "https://www.u-blox.com/en/product-resources?field_product_tech=All&field_product_form=All&edit-submit-product-search=Go&f[0]=field_file_category%3A223"
        ]

    def parse(self, response):
        div_list = response.xpath('//div[@class ="view-content"]/div')
        for div_info in div_list:
            href = div_info.xpath('./div/span/div/div/div[1]/div[2]/h2/a/@href').extract()
            if href:
                absurl = href[0]
                filename = absurl.split("/")[-1]
                desc = div_info.xpath('./div/span/div/div/div[1]/div[2]/h2/a/text()').extract()[0]
                productModel = desc.split(" ")[0]

                publish_Time = div_info.xpath('./div/span/div/div/div[1]/div[3]/p/text()').extract()
                if publish_Time:
                    publishTime = publish_Time[0].strip()
                else:
                    publishTime = ""

            elif div_info.xpath('./div/span/div/div/div[1]/div[1]/h2/a/@href').extract():
                href = div_info.xpath('./div/span/div/div/div[1]/div[1]/h2/a/@href').extract()
                absurl = href[0]
                filename = absurl.split("/")[-1]
                desc = div_info.xpath('./div/span/div/div/div[1]/div[1]/h2/a/text()').extract()[0]
                productModel = desc.split(" ")[0]
                publish_Time = div_info.xpath('./div/span/div/div/div[1]/div[2]/p/text()').extract()
                if publish_Time:
                    publishTime = publish_Time[0].strip()
                else:
                    publishTime = ""

            else:
                productModel= ""
                absurl = ""
                desc = ""
                publishTime = ""
                filename = ""

            # print absurl
            # print filename
            # print publishTime
            # print desc
            # print productModel

            item = MI.FirmcrawlerItem()
            item["productVersion"] = ""
            item["productClass"] = ""
            item["productModel"] = productModel
            item["description"] = desc
            item["url"] = absurl
            item["firmwareName"] = filename
            item["publishTime"] = publishTime
            item["crawlerTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["manufacturer"] = "u-blox"
            yield item
            print "firmwarename:", item["firmwareName"]