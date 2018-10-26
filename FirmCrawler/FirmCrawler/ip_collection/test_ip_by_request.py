
import requests

proxy = {
    "http":'http://113.110.47.11:61234'
}

try:
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Connection': 'keep-alive'}
    result = requests.get('https://blog.csdn.net/tingfenyijiu/article/details/77937481', headers = head, proxies=proxy)
    print result
    print result.text
except:
    print 'connect failed'
else:
    print 'success'