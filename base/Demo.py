import urllib.request

#要爬取的网页链接
url = 'http://www.baidu.com'
response = urllib.request.urlopen(url);
print(response.read())

























# #POST
# import urllib.request
#
# #要爬取的网页链接
# url = 'http://www.baidu.com'
# values = {"username":"13093765253","password":"123456"}
# postData = urllib.parse.urlencode(values)
# postData = postData.encode('utf-8')
# response = urllib.request.urlopen(url, postData);
#
# print(response.read())