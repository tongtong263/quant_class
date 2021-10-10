"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 本节课程内容
- groupby操作
- 计算大小
- 获取指定group
- 常见函数
- group内部计算
- 遍历group
"""

import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# =====导入数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_stock_2019\data\a_stock_201903.csv',
    encoding='gbk',
    skiprows=1
)

# print(df)

# ===== groupby常用操作汇总
# 根据'交易日期'进行group，将相同'交易日期'的行放入一个group，
# print(df.groupby('交易日期'))  # 生成一个group对象。不会做实质性操作，只是会判断是否可以根据该变量进行groupby

# group后可以使用相关函数，size()计算每个group的行数
# print(df.groupby('交易日期').size())  # 每天交易的股票数目
# 根据'股票代码'进行group，将相同'股票代码'的行放入一个group，
# print(df.groupby('股票代码').size())  # 每个股票交易的天数


# 获取其中某一个group
# print(df.groupby('交易日期').get_group('2019-03-25'))
# print(df.groupby('股票代码').get_group('sh600000'))


# 其他常见函数
# print(df.groupby('股票代码').describe())  # 只会对数值变量进行describe
# print(df.groupby('股票代码').head(3))
# print(df.groupby('股票代码').tail(3))  # 每个group里面的行顺序，会保留。
# print(df.groupby('股票代码').first())
# print(df.groupby('股票代码').last())
# print(df.groupby('股票代码').nth(2))
# 将group变量不设置为index
# print(df.groupby('股票代码', as_index=False).nth(2))


# 在group之后，取一部分变量进行计算
# 计算每个group的均值
# print(df.groupby('股票代码')['收盘价', '成交量'].mean())
# 计算每个group的最大值
# print(df.groupby('股票代码')['收盘价', '成交量'].max())

# 计算每个group的加总
# print(df.groupby('股票代码')['成交量'].sum())

# 计算该数据在每个group中的排名
# print(df.groupby('交易日期')['成交量'].rank())
# print(df.groupby('交易日期')['成交量'].rank(pct=True))


# 也可以同时用多个变量来进行group，将这些变量的值都相同的行
# df['交易日期'] = pd.to_datetime(df['交易日期'])
# df.loc[df['交易日期'].dt.day < 15, '月份'] = '上旬'
# df['月份'].fillna(value='下旬', inplace=True)
# print(df)

# print(df.groupby(['股票代码', '月份']).size())


# 我们之前讲过的resample、fillna、apply等常见操作，在group里面都可以进行。
# 这些操作需要大家有一定的积累，若直接在group上进行这些操作不熟练，可以使用已下的方式。


# 遍历group，对每个group进行单独操作，然后将这些group合并起来。
# 语法：for key, group in df.groupby('列名'):

# for code, group in df.groupby('股票代码'):
#     print(code)
#     print(group)

# 以下可以对各个group进行任意操作。
# group.fillna()
# group.apply()

# 操作完之后，将这些group再append起来

# 在一开始不熟练的时候，可以多用遍历每个group的方式
