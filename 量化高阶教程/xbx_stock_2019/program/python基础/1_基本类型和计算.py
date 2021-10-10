"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 本节课程内容
- 注释
- print函数介绍
- 代码执行顺序
- 代码中的换行
- 代码中的空格
- 数字
- 字符串
- 布尔值
- 空值
- 变量名称
- 算术运算
- 比较运算
- 布尔运算
希望以后大家只要看这个程序，就能回想起相关的知识。
"""

# === 注释：python中不会运行的文字（或者说代码）
# 在每一行的开头，加上#，是对该行进行单行注释
# print('hello world')  # 行末注释，在一句程序的末尾，一般用来解释这句话。注意空格。

# · PyCharm快捷键：control + / 多行同时注释或取消注释（mac上是command + /）。
# 尝试同时取消注释或注释下面三行代码
# print('hello world')
# print('hello world')
# print('hello world')


# === print函数介绍：输出内容的重要工具
# print用于在终端上，也就是下面弹窗中，输出内容的工具，学名是全局函数
# print()  # 输出一个空行
# print(1)  # 输出一个1
# print(1, 2)  # 输出一个1和2
# print(1, 2, 3)  # 理论上是可以输出无限个元素，你给多少它终端上就输出多少


# === 代码执行顺序：按照我们写的顺序，依次执行
# print(2)
# print(3)
# print(1)
# 大家可以自己课后调整一下顺序，运行一下，感受一下


# === 代码中的换行
"""
1.空行是没有含义的，不会有任何的输出，也不影响代码的逻辑
2.不空行代码会报错
3.适当的空行可以对我们的代码进行排版
"""
# · 空行
# print(1)
#
# print(2)

# · 不空行会报错
# print(1)print(2)

# · 排版
# 你现在看到的示例代码就是，结合注释，可以相得益彰

# === 代码中的空格
# · 有的空格会产生报错
# print( 1)

# · 有的空格不会产生报错
# print( '邢不行')


# === 数字（integer，float）：int，float，以及一些特定场景下的表达方式
# · int类型的整数
# stock_count = 3000  # 整数，比如我们现在A股一共有3000支股票
# print(stock_count, type(stock_count))  # type()函数的作用是输出变量的类型

# · float类型的浮点数
# stock_price = 10.28  # 浮点数，某个股票价格是10.28
# print(stock_price, type(stock_price))
# stock_change = .0156  # 浮点数，某个股票涨了1.56%，小数点之前的0可以省略，.0156和0.0156是一样的。
# print(stock_change, type(stock_change))
# stock_change = -0.0237  # 负数的表示方式，涨跌幅-2.37%
# print(stock_change, type(stock_change))

# · 很大的数字，科学记数法
# market_capital = 2.33E11  # 市值，可以使用科学技术发来表示很大的数字
# print(market_capital, type(market_capital))


# === 字符串（string）：str：python中的文字的表达
# · 字符串的定义
# 字符串：以单引号’，双引号”，三引号’’’开始，同样符号结束
# code = 'sh600000'
# print(code, type(code))
# name = "浦发银行"
# print(name, type(name))
# 更多的内容我们之后会有专门的课程讲解


# === 布尔值（Boolean）：bool，只有两个，True和False。大小写敏感
# print(True, False, type(True))


# === 空值：只有一个，None。大小写敏感。表示没有值的值
# print(None, type(None))


# === 变量
# · 变量的定义
# 变量需要名称
# 不要使用a、b、c、aa等无意义的变量名
# 取名规则：首字母需要是字母或下划线，其余部分可以是字母，下划线和数字
# 补充：最新的版本中，放宽了限制，建议大家不要

# 我们上面的例子就是一个比较好的示范


# === 算术符号, + - * / %
# · 以加法为例子，可以把下面的加号变成- * /其他符号。
# stock_count = 3000  # 假设现有3000支股票
# new_stock_count = 7  # 新增7个股票上市
# 3000 + 7 = 3007
# all_stock_count = stock_count + new_stock_count  # 全部股票共有多少只？
# print(all_stock_count)

# · 取余数的操作：%
# print(9 % 4)

# · 乘方操作：**
# print(3 ** 4)
# 提问：假设支付宝每天收益为万分之一，那300天后总收益怎么计算？
# print((1 / 10000 + 1) ** 300)

# · 自运算的快速写法
# stock_count = 3000
# stock_count += 7  # 效果等同于：stock_count = stock_count + 7。可以把加号变成- * /等其他符号。
# print(stock_count)

# · 算术符号可以连接两个不同类型的变量
# print(23 + 7.5)
# print(3 * 'abc')
# print(3 + 'abc')  # TypeError: unsupported operand type(s) for +: 'int' and 'str'


# === 比较运算：> < >= <= == !=
# num1 = 10
# num2 = 20
# print(num1 > num2)  # 判断num1是否大于num2，输出结果是布尔变量
# print(num1 >= num2)  # 判断num1是否大于等于num2
# print(num1 == num2)  # 判断num1是否等于num2
# print(num1 != num2)  # 判断num1是否不等于于num2


# ===布尔运算：and和or
# · and：两者都为真，才是真
# print((2 > 1) and (2 != 1))  # 两者都是True，输出结果就是True
# print((2 > 1) and (2 == 1))

# · or：至少一个为真，就是真
# print((2 > 1) or (2 == 1))  # 其中有一个为True，输出结果就是True
