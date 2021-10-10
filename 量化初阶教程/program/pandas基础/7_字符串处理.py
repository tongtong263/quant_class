"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- pandas中的字符串的常见操作
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\sgwat\Desktop\quant_class\xbx_stock_2019\data\a_stock_201903.csv',
    encoding='gbk',
    # skiprows=1
)

# =====字符串处理
# print(df['股票代码'])
# print('sh600000'[:2])
# print(df['股票代码'].str[:2])
# print(df['股票代码'].str.upper())  # 加上str之后可以使用常见的字符串函数对整列进行操作
# print(df['股票代码'].str.lower())
# print(df['股票代码'].str.len())  # 计算字符串的长度,length
# df['股票代码'].str.strip()  # strip操作，把字符串两边的空格去掉
# print(df['股票代码'])
# print(df['股票代码'].str.contains('767'))  # 判断字符串中是否包含某些特定字符
# print(df['股票代码'].str.replace('sz', 'sh'))  # 进行替换，将sz替换成sh
# 更多字符串函数请见：http://pandas.pydata.org/pandas-docs/stable/text.html#method-summary
