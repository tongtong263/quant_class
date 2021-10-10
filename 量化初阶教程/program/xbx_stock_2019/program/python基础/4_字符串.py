"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 字符与字符串
- 字符串中的转义
- 字符串常见操作

功能：希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# =====字符
# class_name = '邢不行'
# code = 'sh600000'
# name = '浦发银行'
# email = 'example@quantclass.cn'
# phone = '18820198888'

# =====字符串转义，特殊字符的表达
# print('what is up')  # 如何输入what's up
# print('what\'s up\t')  # 使用\对特殊字符进行转义。转义也可以用于表达不可见字符，例如tab符号：\t。
# print('\\')  # 如果要表达\本身，也需要转义，写为\\。
# print(r'what\'s up')  # 在字符串的开始加r（Raw String），使得字符串中不发生转义。

# =====字符串常见操作：字符串相加，相乘
# str1 = 'abc'
# str2 = 'def'
# print(str1 + str2)  # 字符串可以直接相加
# print(str1 * 3)  # 字符串可以乘以整数
# print('*' * 30)


# =====字符串常见操作：startswith、endswith
# stock_code = 'sh600000'
# print(stock_code.startswith('sh'))  # 判断字符串是否是以'sh'开头
# print(stock_code.startswith('s'))
# print(stock_code.startswith('01'))
# print(stock_code.endswith('0000'))


# =====字符串常见操作：判断
# name = '邢不行'
# print('不' in name)  # 判断字符串中是否包含'邢'
# print('x' in name)


# =====字符串常见操作：替换
# stock_code = 'sh000001'
# stock_code.replace('被替换的值', '替换成的值')
# print(stock_code.replace('sh', 'sz'))  # 于是变成了平安银行
# print('邢不行, 邢不行量化'.replace('邢不行', '西蒙斯'))  # 会替换所有的


# =====字符串常见操作：split
# info = 'sh600000, sz000001, sh600004'
# print(info.split(', '), type(info.split(', ')))
# print(info.split(', ')[0])
# print(info.split('sh600004'))
# 逆操作
# list_var = ['邢', '不', '行', '量', '化', '课', '程']
# print(list_var)
# print(''.join(list_var))


# =====字符串常见操作：strip
# phone = ' 188 2019 8888'
# print(phone)
# print(phone.strip())  # 去除两边的空格
# print(phone.strip('8'))  # 去除两边的空格


# =====字符串的选取：把字符串当做list
# name = '邢不行量化课程'
# print(name[0])
# print(name[:3])
# print(name[3:])
# print(len(name))
# print(name[-1])
