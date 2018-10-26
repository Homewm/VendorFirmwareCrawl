# _*_ coding:utf-8 _*_
__author__ = "zhangguodong"
__time__ = "2018.09.08"

# example1: https://www.jianshu.com/p/588241a313e7
# example2:https://blog.csdn.net/tingfenyijiu/article/details/77937481

import urllib2
import re


class TestProxy(object):
    proxy_ip = [
    '182.32.159.46:808',
    '61.135.217.7:80',

    ]

    def __init__(self):
        self.ip = '61.135.217.7'
        self.port = '80'
        self.url = 'http://www.baidu.com'
        self.timeout = 3
        self.regex = re.compile(r'baidu.com')
        self.run()

    def run(self):
        self.linkWithProxy()

    def linkWithProxy(self):
        server = 'http://'+ self.ip + ':'+ self.port
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http':server}))
        urllib2.install_opener(opener)
        try:
            response = urllib2.urlopen(self.url, timeout=self.timeout)
        except:
            print '%s connect failed' % server
            return

        else:
            try:
                str = response.read()
            except:
                print '%s connect failed' % server
                return

            if self.regex.search(str):
                print '%s connect success .......' % server
                print self.ip + ':' + self.port

if __name__ == '__main__':
    Tp = TestProxy()





























