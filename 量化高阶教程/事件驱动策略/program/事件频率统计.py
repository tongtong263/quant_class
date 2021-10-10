"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx2626
# 本节课程内容
12 事件策略
"""
import pandas as pd
import itertools
from Config import *
from Function import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.min_rows', 500)  # 最多显示数据的行数

# 读取一个事件数据并展示
event = 'event_2'
event_df = pd.read_pickle(root_path + f'/data/事件策略event合集/{event}.pkl')

# 导入上证指数，保证指数数据和股票数据在同一天结束，不然会出现问题。
index_data = import_index_data(root_path + '/data/trade_data/index/sh000300.csv', date_start, date_end)

# 统计每天发生事件的次数
event_df = event_df.groupby(['事件日期']).sum()

# 将事件和指数数据merge合并
event_df = pd.merge(left=index_data, right=event_df[event], left_on=['交易日期'], right_on=['事件日期'], how='left')
event_df.fillna(value=0, inplace=True)  # 将没有发生事件的日期填充为0

# 统计事件的数据
result_df = pd.DataFrame()
result_df.loc[event, '总次数'] = event_df[event].sum()  # 计算事件的总次数
result_df['日均次数'] = result_df['总次数'] / event_df.shape[0]  # 计算日均次数 = 总次数/交易日数
result_df.loc[event, '最大值'] = event_df[event].max()  # 区间内单日发生事件的最大值
result_df.loc[event, '中位数'] = event_df[event].median()  # 区间内单日发生事件的中位数
result_df.loc[event, '无事件天数'] = (event_df[event] == 0).sum()  # 计算无事件天数
result_df['无事件占比'] = result_df['无事件天数'] / event_df.shape[0]  # 无事件占比 = 无事件天数/交易日期

# 计算最大连续有事件天数 & 最大连续无事件天数
result_df.loc[event, '最大连续有事件天数'] = max([len(list(v)) for k, v in itertools.groupby(np.where(event_df[event] > 0, 1, np.nan))])  # 最大有事件最大连续天数
result_df.loc[event, '最大连续无事件天数'] = max([len(list(v)) for k, v in itertools.groupby(np.where(event_df[event] == 0, 1, np.nan))])  # 最大无事件最大连续天数
print(result_df)

# 绘图
draw_equity_curve(event_df, '交易日期', {'event': event})
