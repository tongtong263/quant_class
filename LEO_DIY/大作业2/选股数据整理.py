"""
思路：
1. 导出所有股票数据: 添加“涨跌幅” 和 “开盘买入涨跌幅” 两列
2. 导出指数数据：只留有“记忆日期” 和 “指数涨跌幅” 两列
3. 将每个股票数据和指数数据合并：以指数数据为基准，并且填充空值
4. 加入“涨停价”，“一字涨停”， “开盘涨停”
5. 将合并后的数据转成周线数据
本程序产生的关键数据：“下日_开盘买入涨跌幅”，“下周期每天涨跌幅“

"""
from LEO_DIY.大作业2.Functions import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 8000)  # 最多显示数据的行数

# ===数据周期
period_type = 'W'  # W代表周，M代表月

# ===读取所有股票代码的列表
path = r'C:\Users\sgwat\Desktop\quant_class\LEO_DIY\data\All_Stocks'
stock_code_list = get_stock_code_list_in_one_dir(path)

# ===循环读取并且合并
# 导入上证指数，保证指数数据和股票数据在同一天结束，不然会出现问题。
index_data = import_index_data(r'C:\Users\sgwat\Desktop\quant_class\量化高阶教程\xbx_stock_2019\program\构建自己的股票数据库\sh000001.csv')

# 循环读取股票数据
all_stock_data = pd.DataFrame()  # 用于存储 数据

for code in stock_code_list:
    print(code)

    # =读入股票数据
    df = pd.read_csv(path + '\%s.csv' % code, encoding='gbk', skiprows=1, parse_dates=['交易日期'])

    # =计算涨跌幅
    df['涨跌幅'] = df['收盘价'] / df['前收盘价'] - 1
    df['开盘买入涨跌幅'] = df['收盘价'] / df['开盘价'] - 1  # 为之后开盘买入做好准备

    # 大作業2-振幅1：过去20个交易日中的最高价/最低价-1
    df['振幅1'] = df['收盘价'].rolling(20, min_periods=1).max() / df['收盘价'].rolling(20, min_periods=1).min() - 1

    # 大作業2-振幅2：最近20日振幅均值
    df['每日振幅'] = df['最高价'] / df['最低价'] -1
    df['振幅2'] = df['每日振幅'].rolling(20, min_periods=1).mean()
    del df['每日振幅']

    # 将股票和上证指数合并，补全停牌的日期, 去除上市之前的数据，新增数据"是否交易"、"指数涨跌幅"
    df = merge_with_index_data(df, index_data)

    # =计算涨跌停价格，新增“涨停价”，“一字涨停”，“开盘涨停”
    df = cal_if_zhangting_with_st(df)


    # =计算下个交易的相关情况
    df['下日_是否交易'] = df['是否交易'].shift(-1)
    df['下日_一字涨停'] = df['一字涨停'].shift(-1)
    df['下日_开盘涨停'] = df['开盘涨停'].shift(-1)
    df['下日_是否ST'] = df['股票名称'].str.contains('ST').shift(-1)
    df['下日_是否退市'] = df['股票名称'].str.contains('退').shift(-1)
    df['下日_开盘买入涨跌幅'] = df['开盘买入涨跌幅'].shift(-1)


    # =将日线数据转化为月线或者周线，周期内每日涨跌幅合并成list, 其他数据都是拿周期内最后一天的值
    df = transfer_to_period_data(df, period_type=period_type)

    # =对数据进行整理
    # 删除上市的第一个周期
    df.drop([0], axis=0, inplace=True)  # 删除第一行数据
    # 删除2017年之前的数据
    df = df[df['交易日期'] > pd.to_datetime('20061215')]
    # 计算下周期每天涨幅
    df['下周期每天涨跌幅'] = df['每天涨跌幅'].shift(-1)
    del df['每天涨跌幅']

    # =删除不能交易的周期数
    # 删除月末为st状态的周期数
    df = df[df['股票名称'].str.contains('ST') == False]
    # 删除月末有退市风险的周期数
    df = df[df['股票名称'].str.contains('退') == False]
    # 删除月末不交易的周期数
    df = df[df['是否交易'] == 1]
    # 删除交易天数过少的周期数
    df = df[df['交易天数'] / df['市场交易天数'] >= 0.8]
    df.drop(['交易天数', '市场交易天数'], axis=1, inplace=True)


    # 合并数据
    all_stock_data = all_stock_data.append(df, ignore_index=True)


# ===将数据存入数据库之前，先排序、reset_index
all_stock_data.sort_values(['交易日期', '股票代码'], inplace=True)
all_stock_data.reset_index(inplace=True, drop=True)

# 将数据存储到hdf文件
all_stock_data.to_hdf(r'C:\Users\sgwat\Desktop\quant_class\LEO_DIY\data\homework2_'+period_type+'.h5', 'df', mode='w')

# ===注意事项
# 目前我们只根据市值选股，所以数据中只有一些基本数据加上市值。
# 实际操作中，会根据很多指标进行选股。在增加这些指标的时候，一定要注意在这两个函数中如何增加这些指标：merge_with_index_data(), transfer_to_period_data()
# 比如增加：成交量、财务数据
