"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

本节课讲解如何获取股票的实时价格
"""
from urllib.request import urlopen  # python自带爬虫库
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# =====神奇的网址
# 返回一个股票的数据：http://hq.sinajs.cn/list=sz000001，修改股票代码
# 返回一串股票的数据：http://hq.sinajs.cn/list=sh600000,sz000002,sz300001
# 正常网址：https://finance.sina.com.cn/realstock/company/sh600000/nc.shtml,

# =====构建网址
# 正常股票：sh600000 sz000002，退市股票：sh600002 sz000003、停牌股票：sz300124，除权股票：sh600276，上市新股：sz002952
stock_code_list = ['sh600000', 'sz000002', 'sh600002', 'sz000003', 'sz300124', 'sh600276', 'sz002952']
url = "http://hq.sinajs.cn/list=" + ",".join(stock_code_list)

# =====抓取数据
content = urlopen(url).read().decode('gbk')  # 使用python自带的库，从网络上获取信息

# =====将数据转换成DataFrame
content = content.strip()  # 去掉文本前后的空格、回车等
data_line = content.split('\n')  # 每行是一个股票的数据
data_line = [i.replace('var hq_str_', '').split(',') for i in data_line]
df = pd.DataFrame(data_line, dtype='float')  #

# =====对DataFrame进行整理
df[0] = df[0].str.split('="')
df['stock_code'] = df[0].str[0].str.strip()
df['stock_name'] = df[0].str[-1].str.strip()
df['candle_end_time'] = df[30] + ' ' + df[31]  # 股票市场的K线，是普遍以当跟K线结束时间来命名的
df['candle_end_time'] = pd.to_datetime(df['candle_end_time'])

rename_dict = {1: 'open', 2: 'pre_close', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
               8: 'amount', 9: 'volume', 32: 'status'}  # 自己去对比数据，会有新的返现
# 其中amount单位是股，volume单位是元
df.rename(columns=rename_dict, inplace=True)
df['status'] = df['status'].str.strip('";')
df = df[['stock_code', 'stock_name', 'candle_end_time', 'open', 'high', 'low', 'close', 'pre_close', 'amount', 'volume',
         'buy1', 'sell1', 'status']]

print(df)
# =====考察退市、停牌股票
# 根据特征去删除股票数据
# 通过amount来考察？
df = df[df['open'] - 0 > 0.00001]

# 如何区分退市和停牌？可能可以通过pre_close，还有status

# =====考察新上市的股票
# 考察sz002952
# 对于新上市的股票，pre_close指的是发行价

# =====考察除权股票
# 考察sh600276
# 对于今天除权的股票，pre_close不是昨天真正的收盘价，而是交易所计算出来并且公布的昨天的收盘价。
# 有了这个数据，才能算出这个股票真正的涨跌幅
