"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx2626
# 本节课程内容
12 事件策略
"""
import pandas as pd


def cal_rank_factor(df: pd.DataFrame, extra_cols: list):
    df['rank_factor1'] = df['总市值']
    extra_cols.append('rank_factor1')
    return df, extra_cols
