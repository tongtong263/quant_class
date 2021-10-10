"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx2626
# 本节课程内容
12 事件策略
"""
import os

# 文件目录
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '../'))  # 返回根目录文件夹

# 回测开始结束时间
date_start = '2007-01-01'  # 回测开始时间
date_end = '2021-08-31'  # 回测结束时间

# 手续费
c_rate = 1.2 / 10000  # 手续费
t_rate = 1 / 1000  # 印花税

# 策略参数设置
event = 'event_3'
stk_num_limit = 2  # 最大持有股票数，None代表买入所有发生事件的股票
rank_factor = 'rank_factor1'  # 当超过count_limit时，以什么为基准买入  factor_增持比例   factor_市值
ascending = False  # rank_factor的排序方式，TRUE代表升序，FALSE代表降序

# 资金份数、持有周期数
hold_period = 5  # 持有周期
max_cap_num = 3  # 将资金分成多少份，大小不可以超过持有时间
