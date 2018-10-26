# _*_ coding:utf-8 _*_
#file is 'ftp.py' ,sys.path:'FirmCrawer.ftp.FtpDownloadler'
__author__ = 'zhangguodong'
__time__ = '2017.03.18'
import urllib2
from scrapy.http import Response
class FtpDownloadHandler(object):
    def download_request(self,request,spider):
        """:return a deferred for the HTTP download"""
        hander = urllib2.FTPHandler()
        req = urllib2.Request(url=request.url)
        opener = urllib2.build_opener(hander)
        f = opener.open(req)
        b = f.read()
        print len(b)
        respcls = Response(url=request.url,body=b,request=request)
        return respcls
