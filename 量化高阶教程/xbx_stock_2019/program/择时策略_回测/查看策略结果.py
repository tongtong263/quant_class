"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

将择时策略的案例进行封装
"""
from 量化高阶教程.xbx_stock_2019.program.择时策略_回测.Functions import cal_fuquan_price, cal_zhangting_price
from 量化高阶教程.xbx_stock_2019.program.择时策略_回测.Signals import simple_moving_average_signal
from 量化高阶教程.xbx_stock_2019.program.择时策略_回测.Position import position_at_close
from 量化高阶教程.xbx_stock_2019.program.择时策略_回测.Evaluate import equity_curve_with_long_at_close
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读入股票数据
stock_code = 'sh600276'
df = pd.read_csv(r'C:\Users\sgwat\Desktop\quant_class\量化初阶教程\data\历史股票数据库\stock\{}.csv'.format(stock_code),
                 encoding='gbk', skiprows=1, parse_dates=['交易日期'])

# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['交易日期'], inplace=True)
df.drop_duplicates(subset=['交易日期'], inplace=True)
df.reset_index(inplace=True, drop=True)

# 计算复权价格、涨停价格
df = cal_fuquan_price(df, fuquan_type='后复权')
df = cal_zhangting_price(df)

# 参数
para = [20, 80]

# 计算交易信号
df = simple_moving_average_signal(df, para=para)

# 计算实际持仓
df = position_at_close(df)

# 选择时间段
# 截取上市一年之后的数据
df = df.iloc[250 - 1:]  # 股市一年交易日大约250天
# 截图2007年之后的数据
df = df[df['交易日期'] >= pd.to_datetime('20070101')]  # 一般可以从2006年开始

# 计算资金曲线
df = equity_curve_with_long_at_close(df, c_rate=2.5/10000, t_rate=1.0/1000, slippage=0.01)

print(df)

equity_curve = df.iloc[-1]['equity_curve']
equity_curve_base = df.iloc[-1]['equity_curve_base']
print(para, '基础收益: ', equity_curve_base, '策略最终收益：', equity_curve)
