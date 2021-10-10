"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 排序
- 合并
- 去重
- 其他
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\simons\Desktop\xbx_stock_2019\data\a_stock_201903.csv',
    encoding='gbk',
    skiprows=1
)

# =====排序函数
# print(df.sort_values(by=['交易日期'], ascending=1))  # by参数指定按照什么进行排序，acsending参数指定是顺序还是逆序，1顺序，0逆序
# print(df.sort_values(by=['股票代码', '交易日期'], ascending=[1, 0]))  # 按照多列进行排序


# =====两个df上下合并操作，append操作
# df1 = df.iloc[0:10][['交易日期', '股票代码', '收盘价', '成交量']]
# print(df1)
# df2 = df.iloc[5:15][['交易日期', '股票代码', '收盘价', '成交量']]
# print(df2)
# print(df1.append(df2))  # append操作，将df1和df2上下拼接起来。注意观察拼接之后的index。index可以重复
# df3 = df1.append(df2, ignore_index=True)  # ignore_index参数，用户重新确定index
# print(df3)


# =====对数据进行去重
# df3中有重复的行数，我们如何将重复的行数去除？
# print(df3)
# df3.drop_duplicates(
#     subset=['交易日期', '股票代码'],  # subset参数用来指定根据哪类类数据来判断是否重复。若不指定，则用全部列的数据来判断是否重复
#     keep='first',  # 在去除重复值的时候，我们是保留上面一行还是下面一行？first保留上面一行，last保留下面一行，False就是一行都不保留
#     inplace=True
# )
# print(df3)


# =====其他常用重要函数
# df.reset_index(inplace=True, drop=True)  # 重置index
# df.rename(columns={
#     '收盘价': 'close',
#     '开盘价': 'open',
#     '股票代码': 'code',
#     '股票名称': 'name',
#     '交易日期': 'date',
#     '最高价': 'high',
#     '最低价': 'low',
#     '前收盘价': 'prev_close',
#     '成交量': 'volume',
#     '成交额': 'money'}, inplace=True)  # rename函数给变量修改名字。使用dict将要修改的名字传给columns参数
# print(df.empty)  # 判断一个df是不是为空，此处输出不为空
# print(pd.DataFrame().empty)  # pd.DataFrame()创建一个空的DataFrame，此处输出为空
# print(df.T)  # 将数据转置，行变成列，很有用
