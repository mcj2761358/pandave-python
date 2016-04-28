import urllib
import http.cookiejar

#声明一个对象实例保存cookie
cookieObj = http.cookiejar.CookieJar()
#设置一个cookie处理器,负责从服务器下载cookie到本地,并且在发送请求时带上本地cookie
cookieHandler = urllib.request.HTTPCookieProcessor(cookieObj)

#通过handler构建opener
opener = urllib.request.build_opener(cookieHandler);
response = opener.open('http://mobile.umeng.com/apps/load_authorised_apps?per_page=30&page=1&order=&sort_metric=&show_all=false');

for item in cookieObj:
    print('Name = ',item.name)
    print('Value = ',item.value)



