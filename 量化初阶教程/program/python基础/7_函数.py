"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 基本函数的定义
- 调用函数
- 函数的返回值
- 函数的重要意义

功能：本程序主要介绍python的函数
"""

"""
函数是编程当中最常用的概念，其目的是将一段功能完整的代码封装起来，方便之后的反复使用。
"""


# ===== 基本函数的定义
def print_two_var(str_var1, str_var2='hello money'):
    # 以下是函数内容
    # 函数的功能：将str_var1，str_var12变量的内容打印出来
    print(str_var1)
    print(str_var2)

    return '我是print_two_var的返回值'


# 以def开头，代表define
# print_two_var是函数名，可以自己随便取，但是要有意义
# str_var是参数，参数的数量可以有很多个，可以带上默认参数
# 函数首行的最后需要带上冒号，初学最容易忘记
# 函数内容需要使用tab键进行缩进，在键盘左边
# 函数的输出，通过return来返回。运行到return语句之后，整个函数运行结束。return可以不加


# ===== 调用函数
# 直接使用函数名，即可调用函数。
# print_two_var(str_var1='你好，Python')
# print_two_var(str_var1='你好，Python', str_var2='你好，量化投资')

# 函数名不能拼错

# 函数调用的时候，建议把参数名写全，注意顺序
# print_two_var(str_var1='你好，Python', str_var2='你好，量化投资')
# print_two_var(str_var2='你好，量化投资', str_var1='你好，Python')
# print_two_var('你好，Python', '你好，量化投资')
# print_two_var('你好，量化投资', '你好，Python')
# print_two_var('你好，Python')

# 函数需要先定义，再调用

# ===== 函数的return值
# temp = print_two_var(str_var1='你好，Python')
# print(temp)


# ===== 函数的重要意义
# 我们可以定一个一个获取最新股票价格的函数
# 这样就把这个一个特定，逻辑也相对复杂的功能，放在一个函数内
# 要用的时候我们调用函数就好了，这个过程也叫封装
# def get_price(stock_code):
#     """
#     获取最新的股票价格
#     :param stock_code: 股票代码
#     :return:
#     """
#     # 我们假装输出最新的价格，实际过程会复杂的多
#     print(stock_code + '股价是: 12.8')
#     return
