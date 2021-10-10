"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- range函数
- for循环语句
- while循环语句

功能：希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# === range函数
# 产生一个类似于[0, 1, 2, 3, ...]这样的一个列表
# range的用法有：
# 1. range(N)：得到[0, 1, 2, 3, ..., N-1]
# 2. range(a, b)：得到[a, a+1, ..., b - 1]。这边要注意如果a>=b的话，得到的是[]
# 3. 第三种方法我们在有需要的时候给大家介绍，大家知道1和2就可以了，有兴趣可以在课程群内讨论。
# range(10)  # [0, 1, 2, ..., 9]
# print(range(10))  # 指代的是一个list但是这边不会直接输出
# print(list(range(10)))  # 强制转为list
# print(list(range(2, 6)))  # 强制转为list


# === 循环语句
"""
循环语句帮助我们做重复的事情。
理论上重复三遍以上的事情，我们就要考虑使用循环
"""

# === for循环语句介绍
# for循环是最常用的循环语句


# ·案例1：循环输出['sh600000', 'sh600002', 'sh600003', 'sz000001']中的结果
# for code in ['sh600000', 'sh600002', 'sh600003', 'sz000001']:
#     print(code)

# ·案例2：计算1+2+3+……+10
# sum_result = 0  # 用于存储计算的结果
# for number in range(10 + 1):
#     sum_result += number  # 此处需要使用tab按键进行缩进
#     print(number, sum_result)

# ·案例3：批量判断股票代码所在的交易所
# code_list = ['sh600000', 'sh600002', 'sh600003', 'sz000001', '600004']
# for code in code_list:
#     if code.startswith('sh'):
#         print(code, '上交所')
#     elif code.startswith('sz'):
#         print(code, '深交所')
#     else:
#         print(code, '并不是sh和sz开头')

# ·案例4：遍历一个dict中所有的元素
# dict_var = {
#     'code': 'sh000001',
#     'name': '上证指数',
#     'open': 3058.8,
#     'high': 3087.0,
#     'low': 3041.96,
#     'close': 3043.03,
#     'vol': 3.668E9
# }
#
# for key, value in dict_var.items():
#     print(key, value)

# ·案例5：for循环语句高级写法
"""
# 口语化的循环表达
变量名 = [针对循环中临时变量名的操作语句 for 循环中临时变量名 in 列表]
"""
# 我们这边把所有的数字都用四舍五入一下
# change_list = [0.01375654, 0.004547676, 0.037813431]
# change_list_rounded = []
# for change in change_list:
#     change_rounded = round(change, 4)
#     change_list_rounded.append(change_rounded)
#
# print(change_list_rounded)
#
# change_list_rounded = [round(change, 4) for change in change_list]
# print(change_list_rounded)


# =====while语句
# while语句语法如下：
"""
while 条件A:
    执行相关操作1（需要使用tab缩进）
    ......
"""

# 条件语句解释说明如下：
"""
1. 判断条件A，若条件A为False，那么程序结束。
2. 判断条件A，若条件A为True，那么执行相关操作1。
3. 然后再次判断条件A，重复上面的步骤
"""

# while语句案例1：计算1+2+3+……+10
# num = 1
# max_num = 10
# sum_result = 0  # 存储计算结果
# while num <= max_num:
#     sum_result += num
#     num += 1
#     print(num, sum_result)
#
# print(sum_result, num, max_num)

# while语句案例2：计算1+2+3+……+10
# num = 1
# max_num = 10
# sum_result = 0
# while True:
#     sum_result += num
#     num += 1
#     print(sum_result, num)
#     if num == max_num + 1:
#         break  # 跳出循环，for也适用

# 关于什么时候用for，什么时候用while
