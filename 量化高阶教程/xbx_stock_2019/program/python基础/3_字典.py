"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 字典介绍
- 字典常见操作

功能：本程序主要介绍python的常用内置数据结果，如list、dict等。希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# =====dict介绍
# 使用{}大括号就可以新建一个dict。[]
# dict_var = {}  # 这是一个空dict
# print(dict_var, type(dict_var))

# 具有一系列成对的对象。一个叫做key，一个叫做value。其中的元素(包括key和value)不需要是同类型
# dict_var = {
#     'sh000001': '上证指数',
#     'sz000001': '平安银行',
#     'sz000001': '平安银行2019',
#     'sh600000': '浦发银行'
# }
# print(dict_var)

# 字典是无顺序，key不可重复
# print(dict_var[0])  # 因为没有顺序，所以dict_var[0]并不能取出第0个位置的元素，此处会报错。


# =====dict常见操作：根据key的值，取相应的value的值
# dict_var = {
#     'sh000001': '上证指数',
#     'sz000001': '平安银行',
#     'sh600000': '浦发银行'
# }

# print(dict_var['sh600004'])  # 获取'sh000001'这个key对应的名称
# print(dict_var.get('sh600004'))  # 效果同上

# list_var = ['上证指数', '平安银行', '浦发银行']  # 如果用list，我们可以这样表达


# =====dict常见操作：增加、修改一对key：value
# dict_var = {
#     'sh000001': '上证指数',
#     'sz000001': '平安银行',
#     '600000': '浦发银行',
#     'sh600000': '浦发银行'
# }
# print(dict_var)  # 先看一下

# dict_var['sh600004'] = '白云机场'
# print(dict_var)
# dict_var['sh600004'] = '白云'
# print(dict_var['sh600004'])

# dict_var['sh000001'] = '上证指数'
# dict_var['sz000001'] = '平安银行'
# print(dict_var)  # 看一下更新后的

# =====dict常见操作：判断一个key是不是在dict里面
# print('sh600000' in dict_var)
# print('sh600352' in dict_var)


# =====dict常见操作：输出一个dict中所有的key和value
# print(dict_var.keys())  # 输出所有的key
# print(dict_var.values())  # 输出所有的value

# 如何访问dict中所有元素，我们会在循环的课程中为大家讲解
