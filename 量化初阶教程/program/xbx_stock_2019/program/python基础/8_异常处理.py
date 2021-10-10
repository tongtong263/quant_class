"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 什么是异常处理
- 异常处理的示例

功能：希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""
import random  # 导入系统库random，可以使用一些系统级别的函数
import time  # 导入系统库time，可以使用一些系统级别的函数

# =====异常处理
"""
异常就是报错，报错会让我们的程序停止。
异常指代的是我们认为不会出错，但是因某些原因导致的报错
- 比如SyntaxError就不算是异常
- HttpError（网络异常）很可能就是一个异常
"""

# ·语法
"""
try:
    执行相关语句1
except Exception as e:
    执行相关语句2
else:
    执行相关语句3
"""

# 说明
"""
1. 先尝试执行相关语句1
2. 若在执行语句1的过程中报错，那么执行相关语句2
3. 若在执行语句1的过程中没有报错，那么执行相关语句3
"""


# =====异常处理的一个例子
def buy():
    """
    此程序用于下单买入某个股票，但是买入过程中，程序有80%的概率报错。
    """
    random_num = random.random()  # 0, 1
    print(random_num)
    if random_num < 0.2:
        print('成功买入')
        return
    else:
        raise ValueError('程序报错！')

# buy()

# === 下单买入一只股票，若买入失败的话尝试重新买入，
# 最多尝试五次
# max_try_count = 5
# try_count = 0
#
# while True:
#     try:  # 尝试做以下事情
#         buy()
#     except Exception as e:  # 如果因为各种原因报错
#         print(e)  # 把exception输出出来
#         print('警告！下单出错，停止1秒再尝试')
#         try_count += 1
#         time.sleep(1)
#         if try_count >= max_try_count:
#             print('超过最大尝试次数，下单失败')
#             # 此处需要执行相关程序，通知某些人
#             break
#         else:
#             continue
#     else:  # 如果没有报错
#         try_count = 0
#         print('下单成功了')
#         break
