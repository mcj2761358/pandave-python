import urllib.request
import re
import urllib
import http.cookiejar
import json

url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing'

urlop = urllib.request.urlopen(url, timeout=10)
# 避免程序异常中止,用try..catch处理异常
try:
    allCarInfo = urlop.read().decode('utf-8')

    ####去掉不符合JSON格式的前后缀
    allCarInfo = allCarInfo[14:-1]
    # print(allCarInfo)

    ####将非标准json转成DICT格式
    allCarInfoDict = eval(allCarInfo, type("Dummy", (dict,), dict(__getitem__=lambda s, n: n))())

    ######取出所有车型数据概览数据
    brandCharDict = allCarInfoDict['brand']
    # print(brandCharDict)

    ####根据字符遍历哥哥品牌车型数据
    count = 0
    carInfoUrl = ''
    for brandChar in brandCharDict:
        brandCarList = brandCharDict[brandChar]
        # print(brandCarList);
        ####遍历字符下的所有品牌车型数据
        for brandItem in brandCarList:
            count = count + 1;
            id = brandItem['id']
            carUrl = brandItem['url']
            name = brandItem['name']
            num = brandItem['num']
            print("第", count, "个品牌:id[", id, "],url[", carUrl, "],name[", name, "],num[", num, "]")

            ####遍历品牌下的所有车型数据
            carInfoUrl = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=' + str(
                id);
            carBrandDetailInfo = urllib.request.urlopen(carInfoUrl, timeout=10).read().decode('utf-8')
            # 去掉不符合JSON的后缀
            carBrandDetailInfo = carBrandDetailInfo[14: -1]
            # 将非标准json转成dict格式
            carBrandDetailInfoDict = eval(carBrandDetailInfo,
                                          type("Dummy", (dict,), dict(__getitem__=lambda s, n: n))())
            # 找到cur=1的节点,即为当前查询的品牌车型数据
            brandTempList = carBrandDetailInfoDict['brand']

            for brandCharTemp in brandTempList:
                brandCarTempList = brandTempList[brandCharTemp]
                for brandItemTemp in brandCarTempList:
                    curTem = brandItemTemp['cur']
                    if curTem == 1:
                        brandName = brandItemTemp['name']
                        #品牌车型信息
                        charTypeList = brandItemTemp['child']
                        for charType in charTypeList :
                            charTypeUrl = charType['url']
                            charTypeName = charType['name']

                            #判断是否有child
                            if 'child' in charType.keys():
                                charTypeChildList = charType['child']
                                #车型子车型信息
                                for charTypeChild in charTypeChildList :
                                    charTypeChildUrl = charTypeChild['url']
                                    charTypeChildName = charTypeChild['name']
                                    print("品牌:[",brandName,"]车型[",charTypeName,"]子车型[",charTypeChildName,"]")

                                    #获取保养信息

                            else :
                                print("品牌:[",brandName,"]车型[",charTypeName,"]")
                                #获取保养信息


            # print(brandTempList)

except:
    print('read data error:url=', url)
