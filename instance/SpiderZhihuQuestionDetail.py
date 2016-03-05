import urllib
import urllib.request
import re
import pymysql.cursors

PLATFORAM_NAME = "zhihu";

spiderUrl = 'https://www.zhihu.com/question/30220049'
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

topic = {
    "questionId": questionId,
    "questionTitle": questionTitle,
    "questionSupport": questionSupport
}
# print(topic)

# 获取知乎问题信息(问题ID,点赞数量,答案作者,作者签名,问题答案,创建时间,编辑时间)
answerList = getQuestionAnswers(responseData)
# print("answerList:", answerList)


# ------------------------------------- 将搜集到的数据,插入到数据库 ------------------------------------#
def getConn():
    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='123456',
                           db='pandave',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


# ------------------------------------- 插入话题信息 -------------------------------------#
topicId = None;


# 根据platform_pid和platform_name查询话题是否已经存在
def handleTopic(topic):
    questionId = topic["questionId"]
    questionTitle = topic["questionTitle"]
    questionSupport = topic["questionSupport"]

    conn = getConn()
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT id,title,content,author_name,last_follow_time FROM pandave_topic where platform_tid =%s and platform_name=%s"
            cursor.execute(sql, (questionId, PLATFORAM_NAME))
            result = cursor.fetchone()
            # print("result", result)

            # 如果不存在,则新建一条记录
            # 1. questionId
            # 2. platformName
            # 3. questionTitle
            # 4. questionSupport
            if (result == None):
                print(questionId, "不存在,插入数据到pandave.")
                sql = "INSERT INTO pandave_topic (creator, gmt_create, modifier, gmt_modified, is_deleted, platform_tid, platform_name, title, content, last_follow_time) " \
                      "VALUES (1, now(), 1, now(), 'N', %s, %s, %s, %s, now());"
                cursor.execute(sql, (questionId, PLATFORAM_NAME, questionTitle, questionSupport))
                conn.commit()

                # 查询出topicId
                sql = "SELECT id,title,content,author_name,last_follow_time FROM pandave_topic where platform_tid =%s and platform_name=%s"
                cursor.execute(sql, (questionId, PLATFORAM_NAME))
                result = cursor.fetchone()
                if result == None:
                    print("话题[",questionId,"]不存在.")
                else :
                    topicId = result["id"]
                print("插入一条新的话题[", topicId, ":", questionId, "]")
            else:
                topicId = result["id"]
                print("话题[", topicId, ":", questionId, "]已存在,判断是否需要更新.")
                # 判断questionTitle和questionSupport是否有变化,如果有变化,做更新,否则,直接跳过.
                id = result["id"]
                resQuestionTitle = result["title"]
                resQuestionSupport = result["content"]

                # 参数说明
                # 1. questionTitle
                # 2. questionSupport
                # 3. id
                if (questionTitle != resQuestionTitle or questionSupport != resQuestionSupport):
                    print("话题数据变化,开始更新话题数据[", topicId, ":", questionId, "].")
                    sql = "update pandave_topic " \
                          "set gmt_modified=now()," \
                          "title=%s,content=%s," \
                          "last_follow_time=now() " \
                          "where id=%s"
                    cursor.execute(sql, (questionTitle, questionSupport, id))
                    conn.commit()
                    print("话题更新成功[", topicId, ":", questionId, "]")


    finally:
        conn.close()

    print("话题处理完成[", topicId, ":", questionId, "]")


# 处理话题回复信息
def handleTopicAnswer(answerList, topicId, questionId):
    if answerList == None:
        print("话题[", topicId, ":", questionId, "]不存在任何回复.")
        return
    else:

        conn = getConn()
        try:
            with conn.cursor() as cursor:

                for answer in answerList:
                    answerId = answer["answerId"]
                    voteCount = answer["voteCount"]
                    answerAuthor = answer["answerAuthor"]
                    answerAuthorLink = answer["answerAuthorLink"]
                    answerAuthorSign = answer["answerAuthorSign"]
                    answerContent = answer["answerContent"]
                    createDate = answer["createDate"]
                    editDate = answer["editDate"]  # 点赞数量超过1000则处理
                    print("voteCount:", voteCount)
                    if int(voteCount) > 1000:
                        print("回复[", answerId, "]超过1000赞,开始数据处理.")

                        # 判断该回答是否已存在,如果不存在,则插入,如果已存在,则更新信息
                        sql = "select id,topic_id,platform_aid,author_name," \
                              "author_id,author_sign,content,answer_create_time," \
                              "answer_modify_time,vote_count,comment_count from pandave_topic_answer where topic_id=%s and platform_aid=%s"
                        cursor.execute(sql, (topicId, answerId))
                        result = cursor.fetchone()
                        if result == None:
                            print("回复[", answerId, "]不存在,插入数据.")
                            # 1. topicId
                            # 2. answerId
                            # 3. answerAuthor
                            # 4. answerAuthorLink
                            # 5. answerAuthorSign
                            # 6. answerContent
                            # 7. createDate
                            # 8. editDate
                            # 9. voteCount
                            sql = "INSERT INTO pandave_topic_answer (creator, gmt_create, modifier, gmt_modified, is_deleted, topic_id, platform_aid, author_name, author_id, author_sign, content, answer_create_time, answer_modify_time, vote_count, comment_count) " \
                                  "VALUES (1, now(), 1, now(), 'N', %s, %s, %s, %s, %s, %s, %s, %s, %s, 0);"
                            cursor.execute(sql, (
                                topicId, answerId, answerAuthor, answerAuthorLink, answerAuthorSign, answerContent,
                                createDate, editDate, voteCount))
                            conn.commit()
                            print("回复[", answerId, "]插入完成.")
                        else:
                            print("更新回复[", answerId, "]数据.")
                            id = result["id"]
                            # 1.answerAuthor
                            # 2.answerAuthorLink
                            # 3.answerAuthorSign
                            # 4.answerContent
                            # 5.createDate
                            # 6.editDate
                            # 7.voteCount
                            # 8.id
                            sql = "update pandave_topic_answer " \
                                  "set gmt_modified=now()," \
                                  "author_name=%s," \
                                  "author_id=%s," \
                                  "author_sign=%s," \
                                  "content=%s," \
                                  "answer_create_time=%s," \
                                  "answer_modify_time=%s," \
                                  "vote_count=%s " \
                                  "where id =%s"
                            cursor.execute(sql, (
                            answerAuthor, answerAuthorLink, answerAuthorSign, answerContent, createDate, editDate, voteCount,
                            id))
                            conn.commit()
                    else:
                        print("回复[", answerId, "]赞的数量不超过1000.")
        finally:
            conn.close()


handleTopic(topic)
handleTopicAnswer(answerList, topicId, questionId)
