"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

存放实盘交易相关的代码
"""
import json
import os
import time
import pandas as pd
from datetime import datetime, timedelta
from urllib.request import urlopen  # python自带爬虫库
import requests

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====获取数据相关函数
# 函数：从网页上抓取数据
def get_content_from_internet(url, max_try_num=10, sleep_time=5):
    """
    使用python自带的urlopen函数，从网页上抓取数据
    :param url: 要抓取数据的网址
    :param max_try_num: 最多尝试抓取次数
    :param sleep_time: 抓取失败后停顿的时间
    :return: 返回抓取到的网页内容
    """
    content = None  # 初始化content为空

    # 抓取内容
    for i in range(max_try_num):
        try:
            content = urlopen(url=url, timeout=10).read()  # 使用python自带的库，从网络上获取信息
            break
        except Exception as e:
            print('抓取数据报错，次数：', i + 1, '报错内容：', e)
            time.sleep(sleep_time)

    # 判断是否成功抓取内容
    if content is not None:
        return content
    else:
        raise ValueError('使用urlopen抓取网页数据不断报错，达到尝试上限，停止程序，请尽快检查问题所在')


# 函数：从新浪获取指定股票的数据
def get_today_data_from_sinajs(code_list):
    """
    返回一串股票最近一个交易日的相关数据
    从这个网址获取股票数据：http://hq.sinajs.cn/list=sh600000,sz000002,sz300001
    正常网址：https://finance.sina.com.cn/realstock/company/sh600000/nc.shtml,
    :param code_list: 一串股票代码的list，可以多个，例如[sh600000, sz000002, sz300001],
    :return: 返回一个存储股票数据的DataFrame
           股票代码  股票名称       交易日期    开盘价    最高价    最低价    收盘价   前收盘价          成交量           成交额   buy1  sell1
0  sz000002  万 科Ａ 2019-05-08  27.42  28.01  27.26  27.39  27.98   35387944.0  9.767760e+08  27.39  27.40
1  sh601288  农业银行 2019-05-08   3.64   3.64   3.61   3.61   3.66  245611404.0  8.892762e+08   3.61   3.62
    """
    # 构建url
    url = "http://hq.sinajs.cn/list=" + ",".join(code_list)

    # 抓取数据
    content = get_content_from_internet(url)
    content = content.decode('gbk')

    # 将数据转换成DataFrame
    content = content.strip()  # 去掉文本前后的空格、回车等
    data_line = content.split('\n')  # 每行是一个股票的数据
    data_line = [i.replace('var hq_str_', '').split(',') for i in data_line]
    df = pd.DataFrame(data_line, dtype='float')  #

    # 对DataFrame进行整理
    df[0] = df[0].str.split('="')
    df['股票代码'] = df[0].str[0].str.strip()
    df['股票名称'] = df[0].str[-1].str.strip()
    df['交易日期'] = df[30]  # 股票市场的K线，是普遍以当跟K线结束时间来命名的
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    rename_dict = {1: '开盘价', 2: '前收盘价', 3: '收盘价', 4: '最高价', 5: '最低价', 6: 'buy1', 7: 'sell1',
                   8: '成交量', 9: '成交额', 32: 'status'}  # 自己去对比数据，会有新的返现
    # 其中amount单位是股，volume单位是元
    df.rename(columns=rename_dict, inplace=True)
    # df['status'] = df['status'].str.strip('";')
    df = df[['股票代码', '股票名称', '交易日期', '开盘价', '最高价', '最低价', '收盘价', '前收盘价', '成交量',
             '成交额', 'buy1', 'sell1']]
    return df


# 函数：从东方财富获取指定股票的涨跌停价格
def get_today_limit_from_eastmoney(stock_code):
    """
    从东方财富网上获取某个股票今天的涨停与跌停价格
    - 正常股票：返回 涨停价，跌停价
    - 停牌股票：返回最近一个交易日的涨跌停价格
    - 退市股票，返回 None，None
    - 不是A股的股票代码，会报 Value Error

    从这个网址获取股票数据：http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292&secid=1.600000&cb=jQuery112404625575479391233_1614321930967&_=1614321930968
    正常网址：http://quote.eastmoney.com/sh600000.html
    优化后的API：http://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=2&fields=f51,f52&secid=1.600000&cb=xxx
    :param stock_code: 股票代码
    :return: 涨停价格，跌停价格
    """
    # 针对股票代码进行格式转换
    if stock_code.startswith('sh'):
        code = '1.' + stock_code[2:]
    elif stock_code.startswith('sz'):
        code = '0.' + stock_code[2:]
    else:
        code = stock_code

    # 构建url
    ts = int(time.time())
    cb = 'jQuery112404625575479391233_%s' % (ts - 1)
    url = 'http://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=2&fields=f51,f52&secid=%s&cb=%s&_=%s' % (
    code, cb, ts)

    # 抓取数据
    content = get_content_from_internet(url)
    content = content.decode('utf-8')

    # 处理返回结果
    content = content.strip()  # 去掉文本前后的空格、回车等
    content = content.replace('%s(' % cb, '')[:-2]
    content = json.loads(content)

    # 当股票是退市股票的时候，返回None，None
    # {'rc': 0, 'rt': 4, 'svr': 182995268, 'lt': 1, 'full': 1, 'data': {'f51': '-', 'f52': '-'}}

    # 获取结果中的涨跌停价格
    up_limit = content['data']['f51']
    down_limit = content['data']['f52']

    # 如果是非正常的A股代码，返回结果为'-'
    if up_limit == '-' or down_limit == '-':
        # 非正常的股票，报错
        return None, None
    else:
        # 正常股票，返回小数类型的涨跌停价格
        return float(up_limit), float(down_limit)


# 函数：获取历史的k线数据
def get_hist_candle_data(stock_code, kline_num=30, folder_path=''):
    """
    根据之前课程5.7中的大作业1，构建了股票数据库。本程序从本地读取指定股票的数据
    :param stock_code: 指定股票代码，例'sh600000'
    :param kline_num: 获取最近K线的数量
    :param folder_path: 数据文件夹；路劲
    :return:
    """
    # 构建存储文件路径
    path = folder_path + '\\' + stock_code + '.csv'

    # 读取数据，数据存在
    if os.path.exists(path):  # 文件存在，不是新股
        df = pd.read_csv(path, encoding='gbk', skiprows=1, parse_dates=['交易日期'])
        df.sort_values(by=['交易日期'], inplace=True)
        df.drop_duplicates(subset=['交易日期'], keep='last', inplace=True)

    # 读取数据，数据不存在
    else:  # 文件不存在，说明是新股
        raise ValueError('读取%s历史数据失败，该地址%s不存在' % (stock_code, path))

    # 获取最近一段数据的K线
    df = df.iloc[-kline_num:]
    df.reset_index(drop=True, inplace=True)

    return df


def get_balance(cli):
    """
    获取balance的时候，银河返回的是list，同花顺返回的是dict
    :param cli: 客户端实例
    :return:
    """
    balance_info = cli.balance
    if isinstance(balance_info, dict):
        return balance_info
    else:
        return balance_info[0]


# =====获取持仓信息相关函数
# 函数：获取单个股票的相关信息
def update_one_stock_info(ths, stock_info):
    """
    获取单个股票的相关信息。注意，不同券商的某些字段会不一样，
    :param ths:
    :param stock_info:
    :return:  {'股票代码': 'sh601258', '交易代码': '601258', '最大买入资金': 100000, '是否交易': True,
    '涨停价格': 1.56, '跌停价格': 1.28, '可用资金': 2763.76, '股票余额': 300, '可用余额': 0}
    """
    # ===获取可用资金
    balance_dict = get_balance(ths)
    time.sleep(0.5)
    stock_info['可用资金'] = balance_dict['可用金额']  # 可以用来买入股票的资金。不同券商，此处字段'可用金额'不一定相同

    # ===获取股票余额，可用余额
    position = pd.DataFrame(ths.position)
    time.sleep(0.5)
    # 更新持仓信息
    if position.empty:
        stock_info['股票余额'] = 0
        stock_info['可用余额'] = 0
    else:
        t = position[position['证券代码'] == stock_info['交易代码']]  # 不同券商，此处字段'证券代码'不一定相同
        if t.empty:
            stock_info['股票余额'] = 0
            stock_info['可用余额'] = 0
        else:
            stock_info['股票余额'] = t.iloc[0]['股票余额']  # 不同券商，此处字段'股票余额'不一定相同
            stock_info['可用余额'] = t.iloc[0]['可用余额']  # 不同券商，此处字段'可用余额'不一定相同

    print('股票情况：\n', stock_info, '\n')


# 函数：获取多个股票的相关信息
def update_account_data(ths, stock_df):
    """
    获取多个股票的相关信息。注意，不同券商的某些字段会不一样，
    :param ths:
    :param stock_df:
    :return:
             分配仓位      股票代码    交易代码  是否交易  涨停价格  跌停价格  股票余额  可用余额   市值   买入成本    参考盈亏      分配资金
交易代码
601288   0.4  sh601288  601288  True  3.96  3.24   200   200  716  3.023  111.47  1868.088
603077   NaN      None    None  None   NaN   NaN     0     0    0   1.89   -8.69       NaN
    """
    # ===更新股票的相关信息
    # 如果update_columns在stock_df中不存在，创建这些columns
    update_columns = ['股票余额', '可用余额', '市值', '买入成本', '参考盈亏']  # 不同券商，此处字段'股票余额'不一定相同
    for c in update_columns:
        if c not in stock_df.columns:
            stock_df[c] = None

    # 获取最新持仓
    position = pd.DataFrame(ths.position)
    time.sleep(0.5)
    # 更新持仓信息
    if position.empty is False:
        position.set_index(keys='证券代码', inplace=True)
        # 补齐不监控，但是账户中存在的股票
        for i in list(set(position.index) - set(stock_df.index)):
            stock_df.loc[i, :] = None
        # 更新stock_df中的数据
        stock_df.update(position)

    # ===获取账户资金的相关信息
    balance_dict = get_balance(ths)
    time.sleep(0.5)
    stock_df_monitor = stock_df[stock_df['分配仓位'].notnull()]
    balance_dict['监控股票盈亏'] = stock_df_monitor['参考盈亏'].sum()
    balance_dict['初始资金'] = balance_dict['总资产'] - balance_dict['监控股票盈亏']
    stock_df['分配资金'] = balance_dict['初始资金'] * stock_df['分配仓位']

    stock_df['股票余额'].fillna(value=0, inplace=True)
    stock_df['可用余额'].fillna(value=0, inplace=True)

    print('股票持仓情况：\n', stock_df, '\n')
    print('账户资金状况：', balance_dict, '\n')
    return balance_dict, stock_df


# =====功能性函数
# 获取最新的卖出价格
def cal_order_price(side, buy1_price, sell1_price, slippage, up_limit_price, down_limit_price):
    if side == 'sell':
        order_price = buy1_price * (1 - slippage)
        order_price = max(round(order_price, 2), down_limit_price)
    elif side == 'buy':
        order_price = sell1_price * (1 + slippage)
        order_price = min(round(order_price, 2), up_limit_price)
    else:
        raise ValueError('side参数必须是 buy 或者 sell')

    return order_price


# 计算复权价格
def cal_fuquan_price(df, fuquan_type='后复权'):
    """
    用于计算复权价格
    :param df: 必须包含的字段：收盘价，前收盘价，开盘价，最高价，最低价
    :param fuquan_type: ‘前复权’或者‘后复权’
    :return: 最终输出的df中，新增字段：收盘价_复权，开盘价_复权，最高价_复权，最低价_复权
    """

    # 计算复权因子
    df['复权因子'] = (df['收盘价'] / df['前收盘价']).cumprod()

    # 计算前复权、后复权收盘价
    if fuquan_type == '后复权':
        df['收盘价_复权'] = df['复权因子'] * (df.iloc[0]['收盘价'] / df.iloc[0]['复权因子'])
    elif fuquan_type == '前复权':
        df['收盘价_复权'] = df['复权因子'] * (df.iloc[-1]['收盘价'] / df.iloc[-1]['复权因子'])
    else:
        raise ValueError('计算复权价时，出现未知的复权类型：%s' % fuquan_type)

    # 计算复权
    df['开盘价_复权'] = df['开盘价'] / df['收盘价'] * df['收盘价_复权']
    df['最高价_复权'] = df['最高价'] / df['收盘价'] * df['收盘价_复权']
    df['最低价_复权'] = df['最低价'] / df['收盘价'] * df['收盘价_复权']
    df.drop(['复权因子'], axis=1, inplace=True)

    return df


# 函数：发送钉钉消息
def send_dingding(message, robot_id='', max_try_count=5):
    """
    出错会自动重发发送钉钉消息
    :param message: 你要发送的消息内容
    :param robot_id: 你的钉钉机器人ID
    :param max_try_count: 最多重试的次数
    """
    try_count = 0
    while True:
        try_count += 1
        try:
            msg = {
                "msgtype": "text",
                "text": {"content": message + '\n' + datetime.now().strftime("%m-%d %H:%M:%S")}}
            headers = {"Content-Type": "application/json;charset=utf-8"}
            url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id
            body = json.dumps(msg)
            requests.post(url, data=body, headers=headers)
            print('钉钉已发送')
            break
        except Exception as e:
            if try_count > max_try_count:
                print("发送钉钉失败：", e)
                break
            else:
                print("发送钉钉报错，重试：", e)


# 函数：获取下一次的运行时间
def next_run_time(time_interval, ahead_seconds=60):
    """
    根据time_interval，计算下次运行的时间，下一个整点时刻
    :param time_interval: 运行的周期，采用pandas中的周期定义方式，例如'15T', '1H'
    :param ahead_seconds: 预留的目标时间和当前时间的间隙
    :return: 下次运行的时间
    案例：
    15T  当前时间为：12:50:51  返回时间为：13:00:00
    15T  当前时间为：12:39:51  返回时间为：12:45:00
    10T  当前时间为：12:38:51  返回时间为：12:40:00
    5T  当前时间为：12:33:51  返回时间为：12:35:00

    5T  当前时间为：12:34:51  返回时间为：12:40:00

    30T  当前时间为：21日的23:33:51  返回时间为：22日的00:00:00

    30T  当前时间为：14:37:51  返回时间为：14:56:00
    """
    ti = pd.to_timedelta(time_interval)
    # now_time = datetime(2019, 5, 9, 12, 50, 30)
    now_time = datetime.now()
    this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    min_step = timedelta(minutes=1)

    target_time = now_time.replace(second=0, microsecond=0)

    while True:
        target_time = target_time + min_step
        delta = target_time - this_midnight
        if delta.seconds % ti.seconds == 0 and (target_time - now_time).seconds >= ahead_seconds:
            # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
            break

    # 针对股票市场，如果下次运行时间正好是收盘时间，做特殊处理
    if target_time.hour == 15 and target_time.minute == 0:  # 下午收盘，提前几分钟
        target_time -= timedelta(minutes=4)
    if target_time.hour == 11 and target_time.minute == 30:  # 上午收盘，提前几分钟
        target_time -= timedelta(minutes=3)

    print('程序下次运行的时间：', target_time, '\n')
    return target_time
