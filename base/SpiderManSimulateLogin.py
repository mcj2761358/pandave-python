import urllib
import http.cookiejar

fileName = 'zhihu.txt'

# 声明一个MozillaCookie.jar保存cookie,之后写入文件
# cookieObj = http.cookiejar.LWPCookieJar(fileName)
cookieObj = http.cookiejar.MozillaCookieJar(fileName)
cookieHandler = urllib.request.HTTPCookieProcessor(cookieObj)
opener = urllib.request.build_opener(cookieHandler)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
           'Referer': 'http://www.zhihu.com/'}

postData ={'email': '907824379@qq.com',
           'password': 'm2761358',
           '_xsrf': '6aa239f077dea8ee10f2050ae1f1b7f2',
            'remember_me': 'true'}

#给post数据编码
postData = urllib.parse.urlencode(postData).encode('utf-8')

# mainpage url
# hostPageUrl = 'https://www.zhihu.com'
# opener.open(hostPageUrl)

postUrl = 'http://www.zhihu.com/login/email'
request = urllib.request.Request(postUrl,postData,headers)
response = opener.open(request)
loginContent = response.read()
print(loginContent.decode('utf-8','ignore'))


# 保存cookie到文件
cookieObj.save(ignore_discard=True, ignore_expires=True)

# 利用cookie请求另一个网站
targetUrl = 'https://www.zhihu.com/topic'
result = opener.open(targetUrl);

content = result.read();

print(content.decode())

