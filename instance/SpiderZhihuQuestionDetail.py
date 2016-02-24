import urllib
import urllib.request
import re
import pymysql

spiderUrl = 'https://www.zhihu.com/question/39880275'
response = urllib.request.urlopen(spiderUrl)
responseData = response.read().decode()


# print(responseData)

### 获取问题唯一编号
def getQuestionId(responseData):
    patternId = re.compile(r'<meta .*?app-argument=zhihu://questions/(.*?)">')
    questionId = re.search(patternId, responseData)
    if questionId:
        questionIdContent = questionId.group(1)
        return questionIdContent


### 获取问题标题
def getQuestionTitle(responseData):
    patternTitle = re.compile(r'<h2 class="zm-item-title zm-editable-content">\s*(.*?)\s*</h2>')
    questionTitle = re.search(patternTitle, responseData)
    if questionTitle:
        questionTitleContent = questionTitle.group(1)
        return questionTitleContent


### 获取问题补充
def getQuestionSupport(responseData):
    patternSupport = re.compile(r'<div class="zm-editable-content">(.*?)</div>')
    questionSupport = re.search(patternSupport, responseData)
    if questionSupport:
        questionSupportContent = questionSupport.group(1)
        return questionSupportContent


### 获取问题答案
def getQuestionAnswers(responseData):
    patternAnswerDiv = re.compile('<div tabindex="-1".*? .*?data-aid="(.*?)".*?>'  # aid
                                  '.*?<a class="zg-anchor-hidden".*?name="(.*?)"></a>.*?'  # aid
                                  '<span class="count">(.*?)</span>.*?'  # voteCount
                                  '<a class="zm-item-link-avatar avatar-link".*?>.*?<img.*?>.*?</a>\s*(.*?)\s*'
                                  '<div class="zm-item-vote-info.*?>.*?'  # author and sign
                                  '<div class="zm-editable-content.*?>\s*(.*?)\s*</div>.*?'  # answer content
                                  '<span class="answer-date-link-wrap">\s*(.*?)\s*</span>.*?'  # answer date
                                  '<a.*?class="meta-item copyright">', re.S)
    answerDivs = re.findall(patternAnswerDiv, responseData)
    answerList = []
    for answerDiv in answerDivs:
        answerId = answerDiv[0]
        voteCount = answerDiv[2]
        answerAuthorText = answerDiv[3]
        answerContent = answerDiv[4]
        answerDateText = answerDiv[5]

        #################### 解析创建日期和编辑日期 ####################
        createDate = None;
        editDate = None;
        patternCreateDate = re.compile(r'<a class="answer-date-link.*?data-tip=".*?发布于(.*?)".*?>编辑于(.*?)</a>')
        resultCreateDate = re.search(patternCreateDate, answerDateText)
        if resultCreateDate:
            createDate = resultCreateDate.group(1)
            editDate = resultCreateDate.group(2)
        else:
            patternCreateDate = re.compile(r'<a class="answer-date-link.*?>发布于 (.*?)</a>')
            resultCreateDate = re.search(patternCreateDate, answerDateText)
            if resultCreateDate:
                createDate = resultCreateDate.group(1)
                editDate = resultCreateDate.group(1)

        #################### 解析作者信息 ####################
        answerAuthor = None
        answerAuthorLink = None
        patternAuthor = re.compile(r'<span class="name">(.*?)</span>')
        resultAuthor = re.search(patternAuthor, answerAuthorText);
        if resultAuthor:
            answerAuthor = resultAuthor.group(1)
        else:
            patternAuthor = re.compile(r'<a.*?href="(.*?)">(.*?)</a>')
            resultAuthor = re.search(patternAuthor, answerAuthorText)
            if resultAuthor:
                answerAuthor = resultAuthor.group(2)
                answerAuthorLink = resultAuthor.group(1)

        #################### 解析作者签名信息 ####################
        answerAuthorSign = None
        patternAuthorSign = re.compile(r'<span title="(.*?)".*?>')
        resultAuthorSign = re.search(patternAuthorSign, answerAuthorText)
        if resultAuthorSign:
            answerAuthorSign = resultAuthorSign.group(1)

        # 构造返回结果
        answerMap = {"answerId": answerId, "voteCount": voteCount, "answerAuthor": answerAuthor,
                     "answerAuthorLink": answerAuthorLink, "answerAuthorSign": answerAuthorSign,
                     "answerContent": answerContent, "createDate": createDate, "editDate": editDate}
        answerList.append(answerMap)
    return answerList


# 知乎问题ID
questionId = getQuestionId(responseData)

# 获取问题标题
questionTitle = getQuestionTitle(responseData)

# 获取问题补充
questionSupport = getQuestionSupport(responseData)
print("questionId=", questionId, ",questionTitle=", questionTitle, ",questionSupport=", questionSupport);

# 获取答案
# getQuestionAnswers(responseData)

# 获取知乎问题信息(问题ID,点赞数量,答案作者,作者签名,问题答案,创建时间,编辑时间)
answerList = getQuestionAnswers(responseData)
print("answerList:", answerList)




# ------------------------------------- 将搜集到的数据,插入到数据库 ------------------------------------#


# ------------------------------------- 插入话题信息 -------------------------------------#
# 根据platform_pid和platform_name查询话题是否已经存在

















































































