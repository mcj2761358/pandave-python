import urllib
import urllib.request

spiderUrl = 'https://www.zhihu.com/question/20899988/answer/76214398';

response = urllib.request.urlopen(spiderUrl)


print(response.read().decode())





