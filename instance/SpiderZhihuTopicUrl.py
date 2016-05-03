import urllib.request
import re
import urllib
import http.cookiejar
from instance import SpiderZhihuQuestionDetail

from collections import deque

queue = deque()
visited = set()

url = 'http://www.zhihu.com/question/27747840'
host = 'http://www.zhihu.com'

queue.append(url)
count = 0

while queue:
    url = queue.popleft() #队首元素出列
    visited |= {url}      #标记为已访问

    print('已经抓取:', str(count), '\t\t正在抓取-----> ' + url)

    #如果以http://www.zhihu.com/question/开头且后面全是数字,则抓取该链接
    spiderUrl = url;
    spiderpattern = re.compile(r'http://www.zhihu.com/question/\d+$')
    results = re.match(spiderpattern,spiderUrl)
    if results is not None :
        SpiderZhihuQuestionDetail.executeTopic(spiderUrl);

    count += 1
    try:
        urlop = urllib.request.urlopen(url, timeout=5)
    except :
        print('打开网页异常:',url)
        continue

    #网页的contentType
    contentType = urlop.getheader('Content-Type')
    if 'html' not in contentType:
        #print("contentType=",contentType," url="+url)
        continue



    #避免程序异常中止,用try..catch处理异常
    try:
        data = urlop.read().decode('utf-8')
    except:
        print('read data error:url=',url)
        continue

    #正则表达式提取页面中的所有队列,并判断是否已经访问过,然后加入待爬列表
    linkre = re.compile('href=\"(.+?)\"')
    for x in linkre.findall(data) :
        # 去除站内引用链接
        if x.startswith("//"):
            #print("站内引用:", x)
            continue
        if x.startswith("/"):
            x = host + x

        # 如果以http开头,并且不再visited里面
        if 'http' in x and x not in visited and x.startswith(host):
            queue.append(x)
            #print('加入队列----> ',x)










