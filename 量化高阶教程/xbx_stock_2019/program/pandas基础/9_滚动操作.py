"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 课程内容
- Rolling操作
- Expanding操作
- 输出到本地文件
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_stock_2019\data\sh600000.csv',
    encoding='gbk',
    skiprows=1
)

# =====rolling、expanding操作
# 计算'收盘价'这一列的均值
# print(df['收盘价'])
# 如何得到每一天的最近3天close的均值呢？即如何计算常用的移动平均线？
# 使用rolling函数
# df['收盘价_3天均值'] = df['收盘价'].rolling(3).mean()
# print(df[['收盘价', '收盘价_3天均值']])
# rolling(n)即为取最近n行数据的意思，只计算这n行数据。后面可以接各类计算函数，例如max、min、std等
# print(df['收盘价'].rolling(3).max())
# print(df['收盘价'].rolling(3).min())
# print(df['收盘价'].rolling(3).std())

# rolling可以计算每天的最近3天的均值，如果想计算每天的从一开始至今的均值，应该如何计算？
# 使用expanding操作
# df['收盘价_至今均值'] = df['收盘价'].expanding().mean()
# print(df[['收盘价', '收盘价_至今均值']])

# expanding即为取从头至今的数据。后面可以接各类计算函数
# print(df['收盘价'].expanding().max())
# print(df['收盘价'].expanding().min())
# print(df['收盘价'].expanding().std())

# rolling和expanding简直是为量化领域量身定制的方法，经常会用到。


# =====输出到本地文件
# print(df)
# df.to_csv('output.csv', encoding='gbk', index=False)
