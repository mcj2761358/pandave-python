import pymysql.cursors


def getConn():
    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='123456',
                           db='pandave',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    return conn
