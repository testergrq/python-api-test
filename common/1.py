# import re
#
# data = {"admin_user": "18566668888", "admin_pwd": "123456"}
# s = '{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
# p1 = "\$\{(.*?)}"
# m = re.search(p1, s)
# print('任意位置开始找，找到一个就返回', m)
# g = m.group()
# print(g)
# g1 = m.group(1)
# print(g1)
# value = data[g1]
# s = re.sub(p1, value, s, count=1)
# print('使用正则表达式查找并且替换：', s)
# l = re.findall(p1, s)
# print('查找全部返回一个列表',l)

class Girls:
    single = False
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def sing(self):
        print(self.name,'会唱歌')

if __name__ == '__main__':
    def dancing(self):
        print('会跳舞')
    g = Girls('mango',18)
    print(g.name)
    g.sing()
    setattr(Girls,'hobby','会swim')#给类或者实例动态添加属性和方法
    setattr(Girls,'dancing',dancing)
    g.dancing()
    print(g.hobby)
    # g2 = Girls('lucy',20)
    # print(g2.hobby)
    # print(getattr(Girls,'hobby'))#根据属性名获取类的属性，当属性不存在的时候，报AttributeError
    # print(hasattr(Girls,'male'))#判断这个类有没这个属性，返回布尔值
    # print(hasattr(Girls,'single'))#判断类是否有这个类属性
    # print(hasattr(g,'name'))#判断对象是否有这个实例属性
    # delattr(g,'name')#删除对象属性
    # print(g.name)
    # delattr(Girls,'single')
    # print(getattr(Girls,'single'))




