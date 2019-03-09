import re
from common.config import ReadConfig

config = ReadConfig()


class Context:
    admin_user = config.get('data', 'admin_user')
    admin_pwd = config.get('data', 'admin_pwd')
    loan_member_id = config.get('data', 'loan_member_id')
    normal_user = config.get('data', 'normal_user')
    normal_pwd = config.get('data', 'normal_pwd')
    normal_member_id = config.get('data', 'normal_member_id')
    member_id1 = config.get('data', 'member_id1')
    pwd1 = config.get('data', 'pwd1')
    pwd3 = config.get('data', 'pwd3')
    member_id2 = config.get('data', 'member_id2')
    loan_id2 = config.get('data', 'loan_id2')
    # member_id3 = config.get('data', 'member_id3')
    # loan_id3 = config.get('data', 'loan_id3')
    # id = config.get('data', 'id')

def replace(s):
    # s是目标字符串
    # d是替换的内容
    p = "\$\{(.*?)}"  # 表达式
    while re.search(p, s):
        m = re.search(p, s)  # 任意位置开始找，找到一个就返回，没找到返回None
        key = m.group(1)  # 取一个组匹配的字符串
        if hasattr(Context, key):
            value = getattr(Context, key)# 利用反射动态的获取类的属性
            s = re.sub(p, value, s, count=1)  # 默认查找全部并替换，count控制次数，0代表全部
        else:
            return None
    return s

if __name__ == '__main__':
    s = '{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
    # data = {"admin_user": "18566668888", "admin_pwd": "123456"}
    # s = replace(s, data)
    s = replace(s)
    print(s)
