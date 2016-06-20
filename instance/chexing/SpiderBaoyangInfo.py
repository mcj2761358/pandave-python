import urllib.request
import re
import urllib
import http.cookiejar
import json

url = 'http://car.bitauto.com/tree_chexing/sb_2593/'


def queryCarTypeBaoYang(url):
    urlop = urllib.request.urlopen(url, timeout=10)
    try:
        baoYangInfo = urlop.read().decode('utf-8')
        # print(baoYangInfo)

        #####使用正则表达式取出车型的关键key,分析后知道关键key在以下文本中(quanxinaodia4l)
        #####getDirectSell(2593,'quanxinaodia4l',bit_locationInfo.cityId,'yc-car-tree-1');
        patternCarKey = re.compile(r'getDirectSell(.*?,(.*?),bit_locationInfo.cityId,.*?);', re.S)
        resultCarKey = re.findall(patternCarKey, baoYangInfo)
        # 取出匹配到的key,取出关键key
        carKey = resultCarKey[0][1]
        # 去掉前后单引号
        carKey = carKey[1:-1]

        carTypeBaoYangUrl = 'http://car.bitauto.com/' + str(carKey) + '/baoyang/'
        # print("保养:" + carTypeBaoYangUrl)
        baoYangDetailInfo = urllib.request.urlopen(carTypeBaoYangUrl, timeout=10).read().decode('utf-8');
        # print(baoYangDetailInfo)

        # 取出script里的数据
        patternScriptData = re.compile(r'<script type="text/javascript">(.*?)</script>', re.S);
        resultScriptData = re.findall(patternScriptData, baoYangDetailInfo)
        # print(resultScriptData[0])

        # 取出所有车型车系的数据
        patternCarSeries = re.compile(r'.*?var.*?groups.*?\[(.*?)\].*?', re.S);
        resultCarSeries = re.findall(patternCarSeries, resultScriptData[0])
        carSeriesList = '[' + str(resultCarSeries[0]) + ']'

        # 遍历车型数据
        for carSeries in eval(carSeriesList):
            groupId = carSeries['GroupID']
            groupName = carSeries['GroupName']
            serialName = carSeries['SerialName']
            defaultCarId = carSeries['DefaulCarID']

            carSeriesBaoYangUrl = 'http://car.bitauto.com/tree_baoyang/Home/GetChartInfo/' + str(defaultCarId)
            # print("养护周期url:" + carSeriesBaoYangUrl)
            print("获取保养信息:系列[", serialName, "],车型[", groupName, "],carId[", defaultCarId, "]养护周期url:" + carSeriesBaoYangUrl)

            carSeriesBaoYangInfo = urllib.request.urlopen(carSeriesBaoYangUrl, timeout=10).read().decode('utf-8')
            # 去除前后双引号
            carSeriesBaoYangInfo = carSeriesBaoYangInfo[1:-1]
            # 去除转义字符\
            carSeriesBaoYangInfo = carSeriesBaoYangInfo.replace('\\', '');

            print(carSeriesBaoYangInfo)
            for carSeriesDetail in eval(carSeriesBaoYangInfo):
                print(carSeriesDetail)

    except:
        print('read data error:url=', url)


queryCarTypeBaoYang(url)
