# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import  pymongo
from FirmCrawler.settings import *
from scrapy.conf import settings
class FirmcrawlerPipeline(object):
    def __init__(self):
        host = settings['MONGO_URI']
        port = settings['MONGO_PORT']
        db_name = settings['MONGO_DATABASE']
        db_collection = settings['MONGO_COLLECTION']
        client = pymongo.MongoClient(host=host,port=int(port))
        db = client[db_name]
        self.post = db[db_collection]
    def process_item(self, item, spider):
        url_exist = self.post.find_one({"url": item.get('url')})
        if not url_exist:
            info = dict(item)
            self.post.insert(info)
        return item
