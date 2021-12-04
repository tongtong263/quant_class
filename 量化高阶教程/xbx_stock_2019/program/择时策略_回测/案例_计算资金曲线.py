"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

通过一个简单的案例策略，来演示如何将实际仓位，转换为资金曲线
"""
import pandas as pd
import numpy as np
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====导入数据
df = pd.read_hdf(r'C:\Users\sgwat\Desktop\quant_class\LEO_DIY\data\pos.h5', key='df')


# =====选取相关时间。
# 截取上市一年之后的数据
df = df.iloc[250-1:]  # 股市一年交易日大约250天

# 截图2007年之后的数据
df = df[df['交易日期'] >= pd.to_datetime('20070101')]

# =====找出开仓、平仓条件
condition1 = df['pos'] != 0
condition2 = df['pos'] != df['pos'].shift(1)
open_pos_condition = condition1 & condition2 #有持仓并且上一周期不持仓，买入

condition1 = df['pos'] != 0
condition2 = df['pos'] != df['pos'].shift(-1)
close_pos_condition = condition1 & condition2 #有持仓并且下一周期不持仓，卖出


# =====对每次交易进行分组
df.loc[open_pos_condition, 'start_time'] = df['交易日期']
df['start_time'].fillna(method='ffill', inplace=True)
df.loc[df['pos'] == 0, 'start_time'] = pd.NaT


# =====开始计算资金曲线
# ===基本参数
initial_cash = 1000000  # 初始资金，默认为1000000元
slippage = 0.01  # 滑点，股票默认为0.01元，etf为0.001元
c_rate = 2.5 / 10000  # 手续费，commission fees，默认为万分之2.5
t_rate = 1.0 / 1000  # 印花税，tax，默认为千分之1

# ===在买入的K线
# 在发出信号的当根K线以收盘价买入
df.loc[open_pos_condition, 'stock_num'] = initial_cash * (1 - c_rate) / (df['前收盘价'] + slippage)

# 实际买入股票数量
df['stock_num'] = np.floor(df['stock_num'] / 100) * 100

# 买入股票之后剩余的钱，扣除了手续费
df['cash'] = initial_cash - df['stock_num'] * (df['前收盘价'] + slippage) * (1 + c_rate)

# 收盘时的股票净值
df['stock_value'] = df['stock_num'] * df['收盘价']

# ===在买入之后的K线
# 买入之后现金不再发生变动
df['cash'].fillna(method='ffill', inplace=True)
df.loc[df['pos'] == 0, ['cash']] = None  #卖出时，现金为none

# 股票净值随着涨跌幅波动
group_num = len(df.groupby('start_time'))

if group_num > 1:
    t = df.groupby('start_time').apply(lambda x: x['收盘价_复权'] / x.iloc[0]['收盘价_复权'] * x.iloc[0]['stock_value'])
    t = t.reset_index(level=[0])
    df['stock_value'] = t['收盘价_复权']

elif group_num == 1:
    t = df.groupby('start_time')[['收盘价_复权', 'stock_value']].apply(lambda x: x['收盘价_复权'] / x.iloc[0]['收盘价_复权'] * x.iloc[0]['stock_value'])
    df['stock_value'] = t.T.iloc[:, 0]

# ===在卖出的K线
# 股票数量变动
df.loc[close_pos_condition, 'stock_num'] = df['stock_value'] / df['收盘价']

# 现金变动
df.loc[close_pos_condition, 'cash'] += df.loc[close_pos_condition, 'stock_num'] * (df['收盘价'] - slippage) * (1 - c_rate - t_rate)

# 股票价值变动
df.loc[close_pos_condition, 'stock_value'] = 0

# ===账户净值
df['net_value'] = df['stock_value'] + df['cash']

# ===计算资金曲线
df['equity_change'] = df['net_value'].pct_change(fill_method=None)
df.loc[open_pos_condition, 'equity_change'] = df.loc[open_pos_condition, 'net_value'] / initial_cash - 1  # 开仓日的收益率
df['equity_change'].fillna(value=0, inplace=True)
df['equity_curve'] = (1 + df['equity_change']).cumprod()

df['equity_curve_base'] = (df['收盘价'] / df['前收盘价']).cumprod()

# ===删除无关数据
# df.drop(['start_time', 'stock_num', 'cash', 'stock_value', 'net_value'], axis=1, inplace=True)

print(df[['股票代码', '股票名称', '交易日期', '最高价', '最低价', '开盘价', '收盘价', '前收盘价', 'pos', 'equity_curve', 'equity_curve_base']])
