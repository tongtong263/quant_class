"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 数据筛选
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    # 该参数为数据在电脑中的路径，
    # 要注意字符串转义符号 \ ，可以使用加r变为raw string或者每一个进行\\转义
    # filepath_or_buffer=r'C:\Users\simons\Desktop\xbx_stock_2019\data\a_stock_201903.csv',
    filepath_or_buffer=r'/Volumes/LaCie/课程资料/quant_class_code/data/a_stock_201903.csv',
    # 编码格式，不同的文件有不同的编码方式，一般文件中有中文的，编码是gbk，默认是utf8
    # ** 大家不用去特意记住很多编码，我们常用的就是gbk和utf8，切换一下看一下程序不报错就好了
    encoding='gbk',
)

# =====数据筛选，根据指定的条件，筛选出相关的数据。
# print(df['股票代码'] == 'sh600000')  # 判断交易股票代码是否等于sh600000
# print(df[df['股票代码'] == 'sh600000'])  # 将判断为True的输出：选取股票代码等于sh600000的行
# print(df[df['股票代码'] == 'sh600000'].index)  # 输出判断为True的行的index
# print(df[df['股票代码'].isin(['sh600000', 'sh600004', 'sz000001'])])  # 选取股票代码等于'sh600000'或'sh600004'或'sz000001'的都行
# print(df[df['收盘价'] < 10.0])  # 选取收盘价小于10的行
# print(df[(df['收盘价'] < 10.0) & (df['股票代码'] == 'AIDUSD')])  # 两个条件，或者的话就是|
