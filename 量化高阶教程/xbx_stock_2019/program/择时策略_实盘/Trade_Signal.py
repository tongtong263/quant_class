"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

择时策略中使用到的signal函数，用于实盘交易
"""
import pandas as pd
from datetime import datetime, timedelta
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====移动平均线策略
# 用于实盘的简单移动平均线策略
def Trade_simple_moving_average_signal(df, para=[20, 120]):
    """
    简单的移动平均线策略。只能做多。
    当短期均线上穿长期均线的时候，做多，当短期均线下穿长期均线的时候，平仓
    :param df:
    :param para: ma_short, ma_long
    :return: 最终输出的df中，新增字段：signal，记录发出的交易信号
    """
    # ===策略参数
    ma_short = para[0]  # 短期均线。ma代表：moving_average
    ma_long = para[1]  # 长期均线

    # ===计算均线。所有的指标，都要使用复权价格进行计算。
    df['ma_short'] = df['收盘价_复权'].rolling(ma_short).mean()
    df['ma_long'] = df['收盘价_复权'].rolling(ma_long).mean()

    # ===找出做多信号
    if df.iloc[-1]['ma_short'] > df.iloc[-1]['ma_long'] and df.iloc[-2]['ma_short'] <= df.iloc[-2]['ma_long']:
        return 1

    # ===找出做多平仓信号
    if df.iloc[-1]['ma_short'] < df.iloc[-1]['ma_long'] and df.iloc[-2]['ma_short'] >= df.iloc[-2]['ma_long']:
        return 0

    # ===当没有信号时，返回空值
    return None


# =====测试信号
def Trade_test_signal():
    """
    发出测试交易信号
    :return:
    """
    now_time = datetime.now()
    # 在10点，卖出股票
    if now_time.hour == 10 and now_time.minute == 0:
        return 0
    # 在11点，买入股票
    elif now_time.hour == 11 and now_time.minute == 0:
        return 1
    # 不满足条件，返回空信号
    return None
