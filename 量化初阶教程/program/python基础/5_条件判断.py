"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 条件语句介绍
- 条件语句示例

功能：希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# =====条件语句介绍
# 条件语句语法如下：
"""
if 条件A（结果为布尔值，True或者False）:
    执行相关操作1（需要使用tab缩进）
    ......

elif 条件B（结果为布尔值，True或者False）:
    执行相关操作2
    ......
else:
    执行相关操作3
"""

# 条件语句解释说明如下：
"""
1. 若条件A为True，那么执行相关操作1，程序结束
2. 若条件A为False，那么判断条件B，若条件B为True，那么执行相关操作2，程序结束
3. 若条件A为False，那么判断条件B，若条件B为False，那么执行相关操作3，程序结束
"""

# 条件语句示例：看看股票是否是ST
"""
知识介绍
ST，这是对连续两个会计年度都出现亏损的公司施行的特别处理。ST即为亏损股。
证监会网址：http://www.csrc.gov.cn/xinjiang/xxfw/tzzsyd/200711/t20071115_88780.htm
"""
# name = '浦发银行'
# if name.startswith('ST'):
#     print(name, '连续两个会计年度都出现亏损')
# print('继续执行你的逻辑')

# 条件语句示例：根据股票代码前缀，判断属于上交所还是深交所
# code = 'sh600000'  # 尝试改成sz000001，或者 600002这样
# if code.startswith('sh'):
#     print(code, '上交所')
# elif code.startswith('sz'):
#     print(code, '深交所')
# else:
#     print(code, '不带有信息')

# 条件语句示例：高级写法
"""
# 口语化的条件表达
变量名 = 满足条件时候要显示的内容 if 条件 else 不满足条件的时候要显示的内容
"""
# change = 0.1
# if change >= 0.1:
# #     status = '涨停'
# # else:
# #     status = '没有涨停'

# status = '涨停' if change >= 0.1 else '没有涨停'
# print(change, status)
