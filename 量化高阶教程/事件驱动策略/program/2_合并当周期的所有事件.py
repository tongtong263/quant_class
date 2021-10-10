import pandas as pd
from program.Function import *
from program.Config import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# =====读取数据
all_stock_data = pd.read_pickle(root_path + '/data/数据整理/all_stock_data.pkl')
all_stock_data = all_stock_data[all_stock_data[event] == 1]  # 只保留选中的事件

# =====当一个周期有多个股票的时候，按照排序规则，保留指定数量的股票
if stk_num_limit:
    # 排序方法可以有很多很多：甚至所有的选股策略都可以作为此处的排序方法。
    all_stock_data['factor_rank'] = all_stock_data.groupby('交易日期')[rank_factor].rank(method='first', ascending=ascending)
    all_stock_data = all_stock_data[all_stock_data['factor_rank'] <= stk_num_limit]
    del all_stock_data['factor_rank']


# =====将一个周期的多个股票，转换到一行中。
all_stock_data['股票代码'] += ' '
group = all_stock_data.groupby('交易日期')
day_event_df = pd.DataFrame()
day_event_df['股票数量'] = group['股票代码'].size()
day_event_df['买入股票代码'] = group['股票代码'].sum()

# =====计算买入每天所有事件股票后的资金曲线
# 第一天的涨跌幅，替换为开盘买入涨跌幅
day_event_df['持仓每日净值'] = group['未来N日涨跌幅'].apply(cal_today_stock_cap_line, hold_period=hold_period)
# 扣除买入手续费
day_event_df['持仓每日净值'] = day_event_df['持仓每日净值'].apply(lambda x: np.array(x) * (1 - c_rate))
# 扣除卖出手续费
day_event_df['持仓每日净值'] = day_event_df['持仓每日净值'].apply(lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)])

day_event_df.to_pickle(root_path + '/data/数据整理/day_event_df.pkl')
print(day_event_df)




