"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

本节课讲解如何获取股票的最近的日K线数据
"""
from urllib.request import urlopen  # python自带爬虫库
import json  # python自带的json数据库
from random import randint  # python自带的随机数库
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====创建随机数的函数
def _random(n=16):
    """
    创建一个n位的随机整数
    :param n:
    :return:
    """
    start = 10**(n-1)
    end = (10**n)-1

    return str(randint(start, end))

# =====获取日、周、月的K线数据
# ===神奇的网址
# 获取K线数据：http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sz000001,day,,,50,qfq&r=0.5643184591626897
# 正常网址：http://stockhtm.finance.qq.com/sstock/ggcx/000001.shtml


# ===构建网址
# 参数
stock_code = 'sh000001'  # 正常股票sz000001，指数sh000001, ETF sh510500
k_type = 'day'  # day, week, month分别对用日线、周线、月线
num = 30000  # 股票最多不能超过640，指数、etf等没有限制

# 构建url
url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_%sqfq&param=%s,%s,,,%s,qfq&r=0.%s'
url = url % (k_type, stock_code, k_type, num, _random())

# ===获取数据
content = urlopen(url).read().decode()  # 使用python自带的库，从网络上获取信息

# ===将数据转换成dict格式
content = content.split('=', maxsplit=1)[-1]
content = json.loads(content)  # 自己去仔细看下这里面有什么数据

# ===将数据转换成DataFrame格式
k_data = content['data'][stock_code]
if k_type in k_data:
    k_data = k_data[k_type]
elif 'qfq' + k_type in k_data:  # qfq是前复权的缩写
    k_data = k_data['qfq' + k_type]
else:
    raise ValueError('已知的key在dict中均不存在，请检查数据')
df = pd.DataFrame(k_data)


# ===对数据进行整理
rename_dict = {0: 'candle_end_time', 1: 'open', 2: 'close', 3: 'high', 4: 'low', 5: 'amount', 6: 'info'}
# 其中amount单位是手，说明数据不够精确
df.rename(columns=rename_dict, inplace=True)
df['candle_end_time'] = pd.to_datetime(df['candle_end_time'])
if 'info' not in df:
    df['info'] = None
df = df[['candle_end_time', 'open', 'high', 'low', 'close', 'amount', 'info']]
print(df)

# ===考察其他周期、指数、ETF

# ===考察特殊情况
# 正常股票：sz000001 sz000002，退市股票：sh600002 sz000003、停牌股票：sz300124，上市新股：sz002952，除权股票：sh600276

