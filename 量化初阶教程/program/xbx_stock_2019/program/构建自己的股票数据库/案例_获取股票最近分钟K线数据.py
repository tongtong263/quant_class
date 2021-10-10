"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

本节课讲解如何获取股票的最近的分钟K线数据
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


# =====获取分钟级别的K线
# 获取K线数据：http://ifzq.gtimg.cn/appstock/app/kline/mkline?param=sz000001,m5,,640&_var=m5_today&r=0.6508601564534552
# 正常网址：http://stockhtm.finance.qq.com/sstock/ggcx/000001.shtml

# ===构建网址
# 参数
stock_code = 'sz002952'  # # 正常股票sz000001，指数sh000001, ETF sh510500
k_type = 60  # 1, 5, 15, 30, 60
num = 1000  # 最多不能超过320

# 构建url
url = 'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param=%s,m%s,,%s&_var=m%s_today&r=0.%s'
url = url % (stock_code, k_type, num, k_type, _random())

# ===获取数据
content = urlopen(url=url, timeout=15).read().decode()  # 使用python自带的库，从网络上获取信息

# ===将数据转换成dict格式
content = content.split('=', maxsplit=1)[-1]
content = json.loads(content)

# ===将数据转换成DataFrame格式
k_data = content['data'][stock_code]['m'+str(k_type)]
df = pd.DataFrame(k_data)

# ===对数据进行整理
rename_dict = {0: 'candle_end_time', 1: 'open', 2: 'close', 3: 'high', 4: 'low', 5: 'amount'}
# 其中amount单位是手
df.rename(columns=rename_dict, inplace=True)
df['candle_end_time'] = df['candle_end_time'].apply(lambda x: '%s-%s-%s %s:%s' % (x[0:4], x[4:6], x[6:8], x[8:10], x[10:12]))
df['candle_end_time'] = pd.to_datetime(df['candle_end_time'])
df = df[['candle_end_time', 'open', 'high', 'low', 'close', 'amount']]
print(df)
# ===考察其他周期、指数、ETF

# ===考察特殊情况
# 正常股票：sz000001 sz000002，退市股票：sh600002 sz000003、停牌股票：sz300124，上市新股：sz002952，除权股票：sh600276，

