# -*- coding: utf-8 -*-

# Scrapy settings for FirmCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FirmCrawler'

SPIDER_MODULES = ['FirmCrawler.spiders']
NEWSPIDER_MODULE = 'FirmCrawler.spiders'


HTTPERROR_ALLOWED_CODES = [403,400,404,502]

DOWNLOADER_MIDDLEWARES = {
    'FirmCrawler.useragentmiddleware.randomUserAgentMiddleWare':401,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware':None
}

#aim to ftp file
DOWNLOAD_HANDLERS ={'ftp':'FirmCrawler.ftp.FtpDownloadHandler'}

#set download delay can use
DOWNLOAD_DELAY = 0.25

ITEM_PIPELINES = {
    'FirmCrawler.pipelines.FirmcrawlerPipeline':300,
}
LOG_LEVEL = 'INFO'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'FirmCrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#get mongodb info
import codecs
import ConfigParser
config = ConfigParser.ConfigParser()
configfile = r'./scrapy.cfg'
config.readfp(codecs.open(configfile,'r','utf-8'))
MONGO_URI = config.get('mongo_cfg',"MONGO_IP")
MONGO_PORT = config.get('mongo_cfg',"MONGO_PORT")
MONGO_DATABASE = config.get('mongo_cfg',"MONGO_DATABASE")
MONGO_COLLECTION = config.get('mongo_cfg',"MONGO_SCRAPY_COLLECTION_NAME")

# #edit by @zhangguodong
# dirs_root = config.get('mogo_cfg',"FIRMWARE_STORE_PATH")
# #file_sile = config.get('mongo_cfg',"")
# configfile =r'./CONFIG.cfg'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'FirmCrawler.middlewares.FirmcrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'FirmCrawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'FirmCrawler.pipelines.FirmcrawlerPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ##########################################################################################
# #myconfig
# firmlist_fc = ["Vipa","Schneider", "Rockwell", "Abb","Siemens"]  # 定义一个工控企业队列
# priority = ["Rockwell"]  # 最高优先级2，把最高优先级的厂商配置到此处


###############################################################################################
# import codecs
# import ConfigParser
# config = ConfigParser.ConfigParser()
# globalconfigfile = r'../GLOBAL_CONFIG.config'
# config.readfp(codecs.open(globalconfigfile, "r", "utf-8"))
# MONGO_URI = config.get('globalinfo',"MONGO_IP")
# MONGO_DATABASE = config.get('globalinfo',"MONGO_DATABASE")
# MONGO_COLLECTION = config.get('globalinfo',"MONGO_SCRAPY_COLLECTION_NAME")
# dirs_root = config.get('globalinfo',"FIRMWARE_STORE_PATH")
# #file_size = config.get('globalinfo',"")
#
# configfile = r'./CONFIG.cfg'
# config.readfp(codecs.open(configfile, "r", "utf-8"))
#
# file_size = config.get('info',"FIRMWARES_SIZE_LIMIT")
# rockwelluser = config.get('info',"ROCKWELL_CRAWL_ACCOUNT")
# rockwellpwd = config.get('info',"ROCKWELL_CRAWL_PASSWORD")