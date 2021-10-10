"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 本节课程内容
- 什么是周期转换
- 转换方法基础版
- 转换方法高阶版
- 数据清理
- 周期参数介绍
"""

import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# === 从hdf中读取1分钟数据
df: pd.DataFrame = pd.read_hdf('a_stock_100.h5', key='sh600000')
print(df.head(20))
# exit()

# 《数据周线转换示意图》


# === 第一种方法：将日线数据转为周线数据
# 将交易日期设定为index
# df.set_index('交易日期', inplace=True)

# 周期转换方法：resample
# rule_type = '1W'  # rule='1W'：意思是一周，意味着转变为周线数据
# period_df = df[['收盘价']].resample(rule=rule_type).last()  # last：取这一周的最后一行数据
#
# # 开、高、低的价格，成交量
# period_df['开盘价'] = df['开盘价'].resample(rule=rule_type).first()
# period_df['最高价'] = df['最高价'].resample(rule=rule_type).max()
# period_df['最低价'] = df['最低价'].resample(rule=rule_type).min()
# period_df['成交量'] = df['成交量'].resample(rule=rule_type).sum()
#
# period_df = period_df[['开盘价', '最高价', '最低价', '收盘价', '成交量']]
# print(period_df)
# exit()

# === 第二种方法：将日线数据转为一周数据
# rule_type = '1W'
# period_df = df.resample(rule=rule_type, on='交易日期', base=0, label='left', closed='left').agg(
#     {
#         '开盘价': 'first',
#         '最高价': 'max',
#         '最低价': 'min',
#         '收盘价': 'last',
#         '成交量': 'sum',
#     }
# )
# period_df = period_df[['开盘价', '最高价', '最低价', '收盘价', '成交量']]
# print(period_df)
# exit()
# base参数：帮助确定转换周期开始的时间
# label='left', closed='left'，建议统一设置成'left'


# === 去除不必要的数据
# 去除一天都没有交易的周
# print(period_df)
# print(df[df['交易日期'] > pd.to_datetime('2000-01-23')])
# exit()
# period_df.dropna(subset=['开盘价'], inplace=True)
# 去除成交量为0的交易周期
# period_df = period_df[period_df['成交量'] > 0]
# print(period_df)


# ===rule的取值
"""
    B       business day frequency
    C       custom business day frequency (experimental)
    D       calendar day frequency
    W       weekly frequency
    M       month end frequency
    SM      semi-month end frequency (15th and end of month)
    BM      business month end frequency
    CBM     custom business month end frequency
    MS      month start frequency
    SMS     semi-month start frequency (1st and 15th)
    BMS     business month start frequency
    CBMS    custom business month start frequency
    Q       quarter end frequency
    BQ      business quarter endfrequency
    QS      quarter start frequency
    BQS     business quarter start frequency
    A       year end frequency
    BA      business year end frequency
    AS      year start frequency
    BAS     business year start frequency
    BH      business hour frequency
    H       hourly frequency
    T       minutely frequency
    S       secondly frequency
    L       milliseonds
    U       microseconds
    N       nanoseconds
"""
