import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from random import randint
import json
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

def _random(n = 16):
    start = 10**(n-1)
    end = 10**n -1
    return randint(start, end)

def get_stock_info_from_internet(stock_code):
    # 参数
    # stock_code = 'sh000001'  # 正常股票sz000001，指数sh000001, ETF sh510500
    k_type = 'day'  # day, week, month分别对用日线、周线、月线
    num = 31  # 股票最多不能超过640，指数、etf等没有限制

    # 构建url
    url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_%sqfq&param=%s,%s,,,%s,qfq&r=0.%s'
    url = url % (k_type, stock_code, k_type, num, _random())

    content = urlopen(url).read().decode()
    # ===将数据转换成dict格式
    content = content.split('=', maxsplit=1)[-1]
    content = json.loads(content)

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
    rename_dict = {0: '交易日期', 1: '开盘价', 2: '收盘价', 3: '最高价', 4: '最低价', 5: 'amount'}
    # 其中amount单位是手，说明数据不够精确
    df.rename(columns=rename_dict, inplace=True)
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df['前收盘价'] = df['收盘价'].shift()
    df['股票代码'] = stock_code
    if 'info' not in df:
        df['info'] = None
    df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '前收盘价']]

    # get the first day of the month
    first_day_of_month = datetime.now().date().replace(day=1)  # replace the day with 01
    date_str = first_day_of_month.strftime("%Y-%m-%d")  # convert datetime to string
    return df[df['交易日期'] >= date_str]


file_path = r'C:\Users\sgwat\Desktop\quant_class\量化初阶教程\data\历史股票数据库\作业3.csv'
df = pd.read_csv(file_path, encoding='gbk')

# 取当月交易天数
trades_info = get_stock_info_from_internet(stock_code='sh000001')
day_count = trades_info['交易日期'].count()

# 取交易天数少于day_count
df = df[df['交易天数']<day_count]
# 去掉开头为N的刚上市股票
df = df[df['股票名称'].str[0] != 'N']
df.reset_index(inplace=True, drop=True)
print(df)

path = 'C:/Users/sgwat/Desktop/quant_class/量化初阶教程/data/历史股票数据库/作业4.csv'
df.to_csv(path, mode='w', index=False, encoding='gbk')
print('saved to 作业4.csv')