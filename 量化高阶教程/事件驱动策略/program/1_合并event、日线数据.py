"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx2626
# 本节课程内容
12.2 事件策略数据整理
将事件策略数据event_df于日线数据合并
"""
from datetime import datetime
from multiprocessing import Pool, cpu_count
from Config import *
from Rank_function import *
from program.Function import *

N_days = 40  # 记录未来N天的收益率
indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=N_days)  # 反向rolling申明变量

# ===读取相关数据
# 批量读取事件数据
event_list = ['event_1', 'event_2', 'event_3']
event_df = read_event_data(root_path + '/data/事件策略event合集', event_list)  # 见excel数据展示
# 事件相关的股票
stock_list = sorted(event_df['股票代码'].drop_duplicates().to_list())
# 读取指数数据，务必使得指数数据和股票数据在同一天结束
index_data = import_index_data(root_path + '/data/trade_data/index/sh000300.csv')


# ===处理单个股票
def cal_with_stock(code):
    print(code)
    # 读取股票数据
    df = pd.read_csv(root_path + '/data/trade_data/stock/%s.csv' % code, encoding='gbk', skiprows=1, parse_dates=['交易日期'])
    # 计算交易天数
    df['交易天数'] = df.index + 1
    # 剔除上市交易日期不足N天的股票
    if df.iloc[-1]['交易天数'] < 250:
        return pd.DataFrame()
    # 计算涨跌幅
    df['涨跌幅'] = df['收盘价'] / df['前收盘价'] - 1
    df['开盘买入涨跌幅'] = df['收盘价'] / df['开盘价'] - 1  # 为之后开盘买入做好准备
    # 和指数合并
    df = merge_with_index_data(df, index_data)
    # 计算涨跌停价格
    df = cal_if_zhangting_with_st(df)
    df = df[['股票代码', '股票名称', '交易日期', '交易天数', '涨跌幅', '开盘买入涨跌幅', '总市值', '一字涨停', '开盘涨停', '是否交易']]

    # ==============================计算事件策略相关代码==============================

    # 读取本股票的事件
    event_data = event_df[event_df['股票代码'] == code].copy()
    # 判断event_data是否为空，如果为空，直接return空的df
    del event_data['股票代码']

    # 将事件数据和日线数据合并。不能简单的上使用merge
    event_data = pd.merge_asof(left=event_data, right=df, left_on=['事件日期'], right_on=['交易日期'], direction='backward')
    # 参考文档：https://pandas.pydata.org/pandas-docs/version/0.25.0/reference/api/pandas.merge_asof.html
    # 删除重复日期：例如周六、周日两天分别触发两次事件，只在周一买一份股票。
    event_data.drop_duplicates(subset=['交易日期'], inplace=True, keep='last')
    df = pd.merge(left=df, right=event_data[['交易日期', '事件日期'] + event_list], on=['交易日期'], how='left', suffixes=('', '_merge'))

    # 实际持仓要晚一天
    for event in event_list:
        df[event] = df[event].shift()
    df['事件日期'] = df['事件日期'].shift()

    # 计算排序因子
    extra_cols = []  # 需要输出的列放这里
    df, extra_cols = cal_rank_factor(df, extra_cols)

    # ==============================计算事件策略相关代码==============================

    # 计算每天未来N日的涨跌幅（包含当天）
    df['涨跌幅'].rolling(window=indexer, min_periods=1)
    df['未来N日涨跌幅'] = [window.to_list() for window in df['涨跌幅'].rolling(window=indexer, min_periods=1)]

    # 某些事件虽然发生，但是当天股票无法买入，所以将该事件强行从1设置为0
    # 这里代码可以优化
    for event in event_list:
        # 删除一些有信号但实际无法买入的
        df.loc[df['股票名称'].str.contains('ST'), event] = 0
        df.loc[df['股票名称'].str.contains('退'), event] = 0
        df.loc[df['一字涨停'] == True, event] = 0
        df.loc[df['开盘涨停'] == True, event] = 0
        df.loc[df['是否交易'] != 1, event] = 0

    # 只保留发生事件的日期
    df = df[df[event_list].sum(axis=1) >= 1]

    # 只保留需要的列，要不然数据会很大
    col = ['交易日期', '事件日期', '股票代码', '股票名称', '交易天数', '开盘买入涨跌幅', '未来N日涨跌幅'] + extra_cols + event_list
    df = df[col]

    return df


if __name__ == '__main__':

    # 试运行单个股票
    cal_with_stock('sh600000')

    # 并行运行所有股票
    # 标记开始时间
    start_time = datetime.now()
    multiply_process = True
    if multiply_process:
        # 开始并行
        with Pool(max(cpu_count() - 2, 1)) as pool:
            # 使用并行批量获得data frame的一个列表
            df_list = pool.map(cal_with_stock, sorted(stock_list))
            print('读入完成, 开始合并', datetime.now() - start_time)
    else:
        df_list = []
        for stock_code in stock_list:
            data = cal_with_stock(stock_code)
            df_list.append(data)

    print('读入完成, 开始合并', datetime.now() - start_time)
    all_stock_data = pd.concat(df_list, ignore_index=True)
    all_stock_data.sort_values(['交易日期', '股票代码'], inplace=True)  # ===将数据存入数据库之前，先排序、reset_index

    # 截取开始时间和结束时间的事件数据
    all_stock_data = all_stock_data[all_stock_data['交易日期'] >= pd.to_datetime(date_start)]
    all_stock_data = all_stock_data[all_stock_data['交易日期'] <= pd.to_datetime(date_end)]
    print(all_stock_data.tail(5))

    all_stock_data.to_pickle(root_path + '/data/数据整理/all_stock_data.pkl')
    print('运行完成:', datetime.now() - start_time)
