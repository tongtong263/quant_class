"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

根据选股数据，进行选股
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from LEO_DIY.大作业2.Functions import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# ===参数设定
select_stock_num = 15  # 选股数量
c_rate = 1.5 / 10000  # 手续费
t_rate = 1 / 1000  # 印花税


# ===导入数据
# 从hdf文件中读取整理好的所有股票数据
df = pd.read_hdf(r'C:\Users\sgwat\Desktop\quant_class\LEO_DIY\data\homework2_W.h5', 'df')
df.dropna(subset=['下周期每天涨跌幅'], inplace=True)


# ===选股
# 删除下个交易日不交易、开盘涨停的股票，因为这些股票在下个交易日开盘时不能买入。
df = df[df['下日_是否交易'] == 1]
df = df[df['下日_开盘涨停'] == False]
df = df[df['下日_是否ST'] == False]
df = df[df['下日_是否退市'] == False]

# 计算选股因子，反转策略：本周期跌幅最大的股票
# df['本周期涨跌幅'] = df['本周期资金曲线'].apply(lambda x: x[-1] - 1)
# df['排名'] = df.groupby('交易日期')['本周期涨跌幅'].rank()

# # 计算选股因子，惯性策略：本周期涨幅最大的股票
# df['本周期涨跌幅'] = df['本周期资金曲线'].apply(lambda x: x[-1] - 1)
# df['排名'] = df.groupby('交易日期')['本周期涨跌幅'].rank(ascending=False)
#
# # # 计算选股因子，换手率：本周期的成交额 / 本周期最后一个交易日收盘时的流通市值
# df['排名'] = df.groupby('交易日期')['换手率'].rank()
#
# # # 计算选股因子，振幅1
# df['排名'] = df.groupby('交易日期')['振幅1'].rank()
#
# # # 计算选股因子，振幅2
df['排名'] = df.groupby('交易日期')['振幅2'].rank()

# 选取排名靠前的股票
df = df[df['排名'] <= select_stock_num]
# print(df.head(6))


# 按照开盘买入的方式，修正选中股票在下周期每天的涨跌幅。
# 即将下周期每天的涨跌幅中第一天的涨跌幅，改成由开盘买入的涨跌幅
df['下日_开盘买入涨跌幅'] = df['下日_开盘买入涨跌幅'].apply(lambda x: [x])
df['下周期每天涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: x[1:])
df['下周期每天涨跌幅'] = df['下日_开盘买入涨跌幅'] + df['下周期每天涨跌幅']
# print(df[['交易日期', '股票名称', '下日_开盘买入涨跌幅', '下周期每天涨跌幅']].head(6))


# ===整理选中股票数据
# 挑选出选中股票
df['股票代码'] += ' '
df['股票名称'] += ' '
group = df.groupby('交易日期')
select_stock = pd.DataFrame()
select_stock['买入股票代码'] = group['股票代码'].sum()
select_stock['买入股票名称'] = group['股票名称'].sum()

# 计算下周期每天的资金曲线
select_stock['选股下周期每天资金曲线'] = group['下周期每天涨跌幅'].apply(lambda x: np.cumprod(np.array(list(x))+1, axis=1).mean(axis=0))
x = df.iloc[:3]['下周期每天涨跌幅']
# print(x)
# print(list(x))  # 将x变成list
# print(np.array(list(x)))  # 矩阵化
# print(np.array(list(x)) + 1)  # 矩阵中所有元素+1
# print(np.cumprod(np.array(list(x)) + 1, axis=1))  # 连乘，计算资金曲线
# print(np.cumprod(np.array(list(x)) + 1, axis=1).mean(axis=0))  # 连乘，计算资金曲线

# 扣除买入手续费
select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'] * (1 - c_rate)  # 计算有不精准的地方
# 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费, 第一天到倒数第二天加上最后一天去除手续费和印花税的值
select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)])

# 计算下周期整体涨跌幅
select_stock['选股下周期涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: x[-1] - 1)
# 计算下周期每天的涨跌幅, 计算公式： 今天-昨天/昨天
select_stock['选股下周期每天涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(pd.DataFrame([1] + x).pct_change()[0].iloc[1:]))

del select_stock['选股下周期每天资金曲线']

# 计算整体资金曲线
select_stock.reset_index(inplace=True)
select_stock['资金曲线'] = (select_stock['选股下周期涨跌幅'] + 1).cumprod()


# ===计算选中股票每天的资金曲线
# 计算每日资金曲线
index_data = import_index_data(r'C:\Users\sgwat\Desktop\quant_class\量化高阶教程\xbx_stock_2019\program\构建自己的股票数据库\sh000001.csv')
equity = pd.merge(left=index_data, right=select_stock[['交易日期', '买入股票代码']], on=['交易日期'],
                  how='left', sort=True)  # 将选股结果和大盘指数合并

equity['持有股票代码'] = equity['买入股票代码'].shift()
equity['持有股票代码'].fillna(method='ffill', inplace=True)
equity.dropna(subset=['持有股票代码'], inplace=True)


equity['涨跌幅'] = select_stock['选股下周期每天涨跌幅'].sum()

del equity['买入股票代码']
equity['equity_curve'] = (equity['涨跌幅'] + 1).cumprod()
equity['benchmark'] = (equity['指数涨跌幅'] + 1).cumprod()

print(equity)
# ===画图
equity.set_index('交易日期', inplace=True)
plt.plot(equity['equity_curve'])
plt.plot(equity['benchmark'])
plt.legend(loc='best')
plt.show()
