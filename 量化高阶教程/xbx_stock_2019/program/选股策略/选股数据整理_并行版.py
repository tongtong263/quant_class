"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

本节课讲解如何整理股票数据，为之后的选股进行准备，
并且使用20191107西蒙斯直播的并行加速的方法
回看地址：https://appr3RLZXlo9494.h5.xeknow.com/st/0mbPG5Flm
"""
from datetime import datetime
from multiprocessing.pool import Pool

from program.选股策略.Functions import *

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# ===数据周期
period_type = 'W'  # W代表周，M代表月

# ===读取所有股票代码的列表
path = '/Users/simons/Desktop/20191107/xbx_stock_2019_all_0924/data/选股策略/xbx_stock_day_data/stock'
stock_code_list = get_stock_code_list_in_one_dir(path)

# ===循环读取并且合并
# 导入上证指数，保证指数数据和股票数据在同一天结束，不然会出现问题。
index_data = import_index_data('/Users/simons/Desktop/20191107/xbx_stock_2019_all_0924/data/选股策略/sh000001.csv')


def calculate_by_stock(code):
    """
    整理数据核心函数
    :param code: 股票代码
    :return: 一个包含该股票所有历史数据的DataFrame
    """
    print(code)

    # =读入股票数据
    df = pd.read_csv(path + '/%s.csv' % code, encoding='gbk', skiprows=1, parse_dates=['交易日期'])

    # =计算涨跌幅
    df['涨跌幅'] = df['收盘价'] / df['前收盘价'] - 1
    df['开盘买入涨跌幅'] = df['收盘价'] / df['开盘价'] - 1  # 为之后开盘买入做好准备

    # =将股票和上证指数合并，补全停牌的日期，新增数据"是否交易"、"指数涨跌幅"
    df = merge_with_index_data(df, index_data)

    # =计算涨跌停价格
    df = cal_if_zhangting_with_st(df)

    # =计算下个交易的相关情况
    df['下日_是否交易'] = df['是否交易'].shift(-1)
    df['下日_一字涨停'] = df['一字涨停'].shift(-1)
    df['下日_开盘涨停'] = df['开盘涨停'].shift(-1)
    df['下日_是否ST'] = df['股票名称'].str.contains('ST').shift(-1)
    df['下日_是否退市'] = df['股票名称'].str.contains('退').shift(-1)
    df['下日_开盘买入涨跌幅'] = df['开盘买入涨跌幅'].shift(-1)

    # =将日线数据转化为月线或者周线
    df = transfer_to_period_data(df, period_type=period_type)

    # =对数据进行整理
    # 删除上市的第一个周期
    df.drop([0], axis=0, inplace=True)  # 删除第一行数据
    # 删除2017年之前的数据
    df = df[df['交易日期'] > pd.to_datetime('20061215')]
    # 计算下周期每天涨幅
    df['下周期每天涨跌幅'] = df['每天涨跌幅'].shift(-1)
    del df['每天涨跌幅']
    # 此处省略，请参考原程序「选股数据整理.py」
    print(code, '计算完成')
    return df  # 返回计算好的数据


# 标记开始时间
start_time = datetime.now()

# ===普通的办法
all_stock_data = pd.DataFrame()
for stock_code in sorted(stock_code_list):
    d = calculate_by_stock(stock_code)
    all_stock_data = all_stock_data.append(d, ignore_index=True)

print(all_stock_data)

# ===并行提速的办法
# with Pool(processes=12) as pool:  # or whatever your hardware can support
#     # 使用并行批量获得data frame的一个列表
#     df_list = pool.map(calculate_by_stock, sorted(stock_code_list))
#     print('读入完成, 开始合并', datetime.now() - start_time)
#     # 合并为一个大的DataFrame
#     all_stock_data = pd.concat(df_list, ignore_index=True)
"""
20191107西蒙斯直播的并行加速的方法
回看地址：https://appr3RLZXlo9494.h5.xeknow.com/st/0mbPG5Flm
"""

all_stock_data.sort_values(['交易日期', '股票代码'], inplace=True)  # ===将数据存入数据库之前，先排序、reset_index
all_stock_data.reset_index(inplace=True, drop=True)

# 将数据存储到hdf文件
all_stock_data.to_hdf(
    '/Users/simons/Desktop/20191107/xbx_stock_2019_all_0924/data/选股策略/all_stock_data_' + period_type + '.h5', 'df',
    mode='w')

# 打印一下benchmark，看一下花了多久
print(datetime.now() - start_time)
# ===注意事项
# 目前我们只根据市值选股，所以数据中只有一些基本数据加上市值。
# 实际操作中，会根据很多指标进行选股。在增加这些指标的时候，一定要注意在这两个函数中如何增加这些指标：merge_with_index_data(), transfer_to_period_data()
# 比如增加：成交量、财务数据
