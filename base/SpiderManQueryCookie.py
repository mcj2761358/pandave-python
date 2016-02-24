import http.cookiejar
import urllib

fileName = 'cookie.txt'
#创建MozillaCookiejar实例
cookieObj = http.cookiejar.MozillaCookieJar()
#从文件中读取cookie内容到内存
cookieObj.load(fileName, ignore_discard=True, ignore_expires=True);


for item in cookieObj:
    print('Name = ',item.name)
    print('Value = ',item.value)








