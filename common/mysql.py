import pymysql
from common.config import ReadConfig

class MysqlUtil:
    def __init__(self, return_dict=False):
        # 1.建立连接
        config = ReadConfig()
        host = config.get('db','host')
        user = config.get('db','user')
        password = config.get('db','password')
        port = config.getint('db','port')
        self.mysql = pymysql.connect(host=host, user=user, password=password, port=port)
        if return_dict:
            self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)#指定每行数据以字典的形式返回
        else:
            self.cursor = self.mysql.cursor()#指定每行数据以元祖的形式返回

    def fetch_one(self, sql):
        # 2.新建一个查询页面
        # 3.执行sql
        self.cursor.execute(sql)
        # 4.查看结果
        result = self.cursor.fetchone()#返回元祖()
        return result#返回最新的一条数据

    def fetch_all(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()#返回列表[(),()]
        return results

    def close(self):
        self.cursor.close()
        self.mysql.close()


if __name__ == '__main__':
    # mysql = MysqlUtil()
    # sql = 'select max(mobilephone) from future.member'
    # result = mysql.fetch_one(sql)
    # print(result[0])
    # mysql.close()
    mysql = MysqlUtil(return_dict=True)
    sql = 'select * from future.member limit 5'
    results = mysql.fetch_one(sql)
    print(results)
    for result in results:
        print(result)
    mysql.close()
