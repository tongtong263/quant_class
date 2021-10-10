from urllib.request import urlopen  # python自带爬虫库
import pandas as pd
from datetime import datetime
import time
import re  # 正则表达式库
import os  # 系统库
import json  # python自带的json数据库
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# get current month data from all csv files
def import_batch_csv_files():
    file_location = r'C:\Users\sgwat\Desktop\quant_class\量化初阶教程\data\历史股票数据库\stock'

    file_list = []
    for root, dirs, files in os.walk(file_location):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                file_path = os.path.abspath(file_path)  # returns a normalized version of the pathname path
                file_list.append(file_path)

    # get the first day of the month
    first_day_of_month = datetime.now().date().replace(day=1)  #replace the day with 01
    date_str = first_day_of_month.strftime("%Y-%m-%d")  # convert datetime to string

    all_data = pd.DataFrame()

    for fp in sorted(file_list):
        # 导入数据
        print('start reading data from ', fp)
        df = pd.read_csv(fp, skiprows=1, encoding='gbk')
        #  合并数据
        all_data = all_data.append(df[df['交易日期'] >= date_str], ignore_index=True)  # 注意此时若一下子导入很多文件，可能会内存溢出

    return all_data

# def get_latest_month_data(31):
#     df = import_batch_csv_files()
#     first_day_month = datetime.now().date().replace(day=1)
#     date_str = first_day_month.strftime("%Y-%m-%d")   # convert datetime to string
#     return df[df['交易日期'] >= date_str]



df = import_batch_csv_files()
df['交易日期'] = pd.to_datetime(df['交易日期'])
df.set_index('交易日期', inplace=True)

all_data = pd.DataFrame()

rule_type = '1M'
for code, group in df.groupby('股票代码'):

    period_df = group[['收盘价', '股票代码', '股票名称']].resample(rule=rule_type).last()  # last：取这一周的最后一行数据

    # 开、高、低的价格，成交量
    period_df['开盘价'] = group['开盘价'].resample(rule=rule_type).first()
    period_df['最高价'] = group['最高价'].resample(rule=rule_type).max()
    period_df['最低价'] = group['最低价'].resample(rule=rule_type).min()
    period_df['成交量'] = group['成交量'].resample(rule=rule_type).sum()
    period_df['成交额'] = group['成交额'].resample(rule=rule_type).sum()
    period_df['交易日期'] = group.index.max()
    period_df['月涨跌幅'] = (period_df['收盘价'] / period_df['开盘价'] -1) * 100
    period_df['交易天数'] = group['成交量'].resample(rule=rule_type).size()

    period_df = period_df[['交易日期', '股票代码', '股票名称', '收盘价', '成交量', '成交额', '月涨跌幅', '交易天数']]
    all_data = all_data.append(period_df)

path = 'C:/Users/sgwat/Desktop/quant_class/量化初阶教程/data/历史股票数据库/作业3.csv'
all_data.to_csv(path, mode='w', index=False, encoding='gbk')
print('saved to 作业3.csv')