"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

更新于：2021-02-26
主要更正了由于数据接口导致的两个问题

本节课讲解如何结合预测者网的历史数据，每天获取股票的数据，
构建完整实时股票数据库。



"""
from urllib.request import urlopen  # python自带爬虫库
import pandas as pd
from datetime import datetime
import time
import re  # 正则表达式库
import os  # 系统库
import json  # python自带的json数据库
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====函数：从网页上抓取数据
def get_content_from_internet(url, max_try_num=10, sleep_time=5):
    """
    使用python自带的urlopen函数，从网页上抓取数据
    :param url: 要抓取数据的网址
    :param max_try_num: 最多尝试抓取次数
    :param sleep_time: 抓取失败后停顿的时间
    :return: 返回抓取到的网页内容
    """
    get_success = False  # 是否成功抓取到内容
    # 抓取内容
    for i in range(max_try_num):
        try:
            content = urlopen(url=url, timeout=10).read()  # 使用python自带的库，从网络上获取信息
            get_success = True  # 成功抓取到内容
            break
        except Exception as e:
            print('抓取数据报错，次数：', i+1, '报错内容：', e)
            time.sleep(sleep_time)


    # 判断是否成功抓取内容
    if get_success:
        return content
    else:
        raise ValueError('使用urlopen抓取网页数据不断报错，达到尝试上限，停止程序，请尽快检查问题所在')


# =====函数：从新浪获取指定股票的数据
def get_today_data_from_sinajs(code_list):
    """
    返回一串股票最近一个交易日的相关数据
    从这个网址获取股票数据：http://hq.sinajs.cn/list=sh600000,sz000002,sz300001
    正常网址：https://finance.sina.com.cn/realstock/company/sh600000/nc.shtml,
    :param code_list: 一串股票代码的list，可以多个，例如[sh600000, sz000002, sz300001],
    :return: 返回一个存储股票数据的DataFrame
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
    df = pd.DataFrame(data_line, dtype='float')

    # 对DataFrame进行整理
    df[0] = df[0].str.split('="')
    df['stock_code'] = df[0].str[0].str.strip()
    df['stock_name'] = df[0].str[-1].str.strip()
    df['candle_end_time'] = df[30] + ' ' + df[31]  # 股票市场的K线，是普遍以当跟K线结束时间来命名的
    df['candle_end_time'] = pd.to_datetime(df['candle_end_time'])  # dtype will change from object to datetime64[ns]
    rename_dict = {1: 'open', 2: 'pre_close', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
                   8: 'volume', 9: 'amount', 32: 'status'}  # 自己去对比数据，会有新的发现
    # 其中amount单位是股，volume单位是元
    df.rename(columns=rename_dict, inplace=True)
    df['status'] = df['status'].astype('str')
    df['status'] = df['status'].str.strip('";')
    df = df[['stock_code', 'stock_name', 'candle_end_time', 'open', 'high', 'low', 'close', 'pre_close', 'amount',
             'volume', 'buy1', 'sell1', 'status']]

    return df


# =====函数：判断今天是否是交易日
def is_today_trading_day():


    """
    判断今天是否是交易日
    :return: 如果是返回True，否则返回False
    """

    # 获取上证指数今天的数据
    df = get_today_data_from_sinajs(code_list=['sh000001'])
    sh_date = df.loc[0]['candle_end_time']  # 上证指数最近交易日
    # 判断今天日期和sh_date是否相同
    print(datetime.now())
    return datetime.now().date() == sh_date.date()

def is_csv_updated():

    """
    从csv文件里拿到茅台的最近交易日期
    """

    # 从csv文件获取茅台的最新一天数据
    df = pd.read_csv(
        r'C:\Users\sgwat\Desktop\quant_class\量化初阶教程\data\历史股票数据库\stock\sh600519.csv',
        encoding='gbk',
        skiprows=1, parse_dates=['交易日期']
    )
    csv_date = df['交易日期'].max()  # 茅台csv文件里最近交易日
    df = get_today_data_from_sinajs(code_list=['sh000001'])
    sh_date = df.loc[0]['candle_end_time']  # 上证指数最近交易日
    return csv_date.date() == sh_date.date()



# =====函数：从新浪获取所有股票的数据
def get_all_today_stock_data_from_sina_marketcenter():
    """
    http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up
    从新浪网址的上述的网址，逐页获取最近一个交易日所有股票的数据
    :return: 返回一个存储股票数据的DataFrame
    """

    # ===数据网址
    raw_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s' \
              '&num=80&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=sort'
    page_num = 1

    # ===存储数据的DataFrame
    all_df = pd.DataFrame()

    # ===获取上证指数最近一个交易日的日期。此段代码在课程视频中没有，之后补上的
    df = get_today_data_from_sinajs(code_list=['sh000001'])
    sh_date = df.iloc[0]['candle_end_time'].date()  # 上证指数最近交易日

    # ===开始逐页遍历，获取股票数据
    while True:
        # 构建url


        url = raw_url % (page_num)
        print('开始抓取页数：', page_num)

        # 抓取数据
        content = get_content_from_internet(url)
        content = content.decode('gbk')

        # 判断页数是否为空
        if '[]' in content or 'null' in content:
            print('抓取到页数的尽头，退出循环')
            break


        # 通过正则表达式，给key加上引号
        content = re.sub(r'(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', content)

        # 将数据转换成dict格式
        content = json.loads(content)

        # 将数据转换成DataFrame格式
        df = pd.DataFrame(content, dtype='float')


        # 对数据进行整理
        # 重命名
        rename_dict = {'symbol': '股票代码', 'name': '股票名称', 'open': '开盘价', 'high': '最高价', 'low': '最低价',
                       'trade': '收盘价', 'settlement': '前收盘价', 'volume': '成交量', 'amount': '成交额', 'nmc': '流通市值',
                       'mktcap': '总市值'}
        df.rename(columns=rename_dict, inplace=True)
        # 添加交易日期
        # df['交易日期'] = pd.to_datetime(datetime.now().date())  # 课程视频中使用的是本行代码
        df['交易日期'] = pd.to_datetime(sh_date)  # 在课程视频中使用的是上一行代码，现在改成本行代码，程序更加稳健

        # 取需要的列
        df = df[['股票代码', '股票名称', '交易日期', '开盘价', '最高价', '最低价', '收盘价', '前收盘价', '成交量', '成交额',
                 '流通市值', '总市值']]

        df['流通市值'] = df['流通市值'] * 10000
        df['总市值'] = df['总市值'] * 10000


        # 合并数据
        all_df = all_df.append(df, ignore_index=True)

        # 将页数+1
        page_num += 1
        time.sleep(1)

    # ===将当天停盘的股票删除，此段代码在课程视频中没有，之后补上的
    all_df = all_df[all_df['开盘价'] - 0 > 0.00001]
    all_df.reset_index(drop=True, inplace=True)

    # ===返回结果
    return all_df

# 判断今天是否是交易日
if is_today_trading_day() is False:
    print('今天不是交易日，不需要更新股票数据，退出程序')
    exit()

# 判断当前时间是否超过15点
if datetime.now().hour < 16:  # 保险起见可以小于16点
    print('今天股票尚未收盘，不更新股票数据，退出程序')
    exit()

# 判断当日日线数据时候已经更新
if is_csv_updated():
    print('CSV已经跟新到最新了，不要重复运行')
    exit()

# 更新数据思路1：
# 1. 使用get_today_data_from_sinajs()从新浪更新股票数据，将数据输出到预测者网的数据中
# 2. 股票代码的list从预测者网数据的文件夹中提取
# 3. 需要考察一下每天新增加的新股代码

# 更新数据思路2：
# 1. 使用get_all_today_stock_data_from_sina_marketcenter()，一下子获取所有股票数据，将数据输出到预测者网的数据中

# 获取今天所有的股票数据

df = get_all_today_stock_data_from_sina_marketcenter()

# 对数据进行存储
for i in df.index:
    t = df.iloc[i:i+1, :]
    stock_code = t.iloc[0]['股票代码']



    # 构建存储文件路径
    path = 'C:/Users/sgwat/Desktop/quant_class/量化初阶教程/data/历史股票数据库/stock/' \
           + stock_code + '.csv'


    # 文件存在，不是新股
    if os.path.exists(path):
        t.to_csv(path, header=None, index=False, mode='a', encoding='gbk')
    # 文件不存在，说明是新股
    else:
        # 先将头文件输出
        pd.DataFrame(columns=['数据由Leo整理']).to_csv(path, index=False, encoding='gbk')
        t.to_csv(path, index=False, mode='a', encoding='gbk')
        print('发现新股票: ', stock_code)

