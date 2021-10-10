"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- 删除缺失值
- 补全缺失值
- 找出缺失值
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\sgwat\Desktop\quant_class\xbx_stock_2019\data\a_stock_201903.csv',
    encoding='gbk',
    skiprows=1
)

# ===== 缺失值处理：原始数据中存在缺失值，如何处理？
# 0.创建缺失值
# index = df[df['交易日期'].isin(['2019-03-01', '2019-03-15'])].index
# df.loc[index, '月头'] = df['交易日期']

# 1.删除缺失值
# print(df.dropna(how='any'))  # 将带有空值的行删除。how='any'意味着，该行中只要有一个空值，就会删除，可以改成all。
# print(df.dropna(subset=['月头', '收盘价'], how='all'))  # subset参数指定在特定的列中判断空值。
# all代表全部为空，才会删除该行；any只要一个为空，就删除该行。

# 2.补全缺失值
# print(df.fillna(value='N'))  # 直接将缺失值赋值为固定的值
# df['月头'].fillna(value=df['收盘价'], inplace=True)  # 直接将缺失值赋值其他列的数据
# print(df.fillna(method='ffill'))  # 向上寻找最近的一个非空值，以该值来填充缺失的位置，全称forward fill，非常有用
# print(df.fillna(method='bfill'))  # 向下寻找最近的一个非空值，以该值来填充确实的位置，全称backward fill

# 3.找出缺失值
# print(df.notnull())  # 判断是否为空值，反向函数为isnull()
# print(df[df['月头'].notnull()])  # 将'月头'列为空的行输出
