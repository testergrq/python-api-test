import pymysql
from common.config import ReadConfig

class MysqlUtil:
    def __init__(self):
        # 1.建立连接
        config = ReadConfig()
        host = config.get('db','host')
        user = config.get('db','user')
        password = config.get('db','password')
        self.mysql = pymysql.connect(host=host, user=user, password=password, port=3306)
        self.cursor = self.mysql.cursor()

    def fetch_one(self, sql):
        # 2.新建一个查询页面
        # 3.执行sql
        self.cursor.execute(sql)
        # 4.查看结果
        result = self.cursor.fetchone()
        return result

    def close(self):
        self.cursor.close()
        self.mysql.close()


if __name__ == '__main__':
    mysql = MysqlUtil()
    sql = 'select max(mobilephone) from future.member'
    result = mysql.fetch_one(sql)
    print(result[0])
    mysql.close()
