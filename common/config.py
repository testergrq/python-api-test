import configparser
from common import contants


class ReadConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()  # 实例化对象
        self.config.read(contants.global_conf, encoding='utf-8')
        open = self.config.getboolean('switch', 'open')
        # print(type(open), open)
        if open:
            self.config.read(contants.test_conf, encoding='utf-8')
        else:
            self.config.read(contants.test2_conf, encoding='utf-8')

    def get(self, session, option):
        try:
            return self.config.get(session, option)
        except configparser.NoSectionError as e:
            print('请查看配置文件是否加载正确')
            raise e

    def getint(self, session, option):
        return self.config.getint(session, option)

    def getfloat(self, session, option):
        return self.config.getfloat(session, option)

    def getboolean(self, session, option):
        return self.config.getboolean(session, option)


if __name__ == '__main__':
    value = ReadConfig().get('api', 'pre_url')
    print(type(value), value)
