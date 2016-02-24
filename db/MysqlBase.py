import pymysql.cursors

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='123456',
                       db='pandave',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)

try:
    # with conn.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO pandave_topic VALUES " \
    #           "(null,1,now(),1,now(),'N',100000,'小熊猫是世界上最美的人吗?','我遇到了一只小熊猫,可爱至极,但是有刺,请问她是最美的人吗?',null,'Minutch','peo-Minutch',null,'2016-01-01','2016-02-01',%s,100,%s)"
    #     cursor.execute(sql,('2016-02-03',12))
    #
    #     # connection is not autocommit by default. so you must commit to save
    #     conn.commit()

    with conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT id,title,content,author_name,last_follow_time FROM pandave_topic"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

finally:
    conn.close()
