"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

一键卖出十个卖出所有股票的所有持仓
"""
import easytrader
import pandas as pd
import time
import warnings
from program.构建自己的股票数据库.每日更新股票数据 import get_today_data_from_sinajs  # 需更改为本电脑路径及地址

pd.set_option('expand_frame_repr', False)
warnings.filterwarnings("ignore")

# =====客户端初始化
user = easytrader.use('yh_client')  # 选择银河客户端

# 输入用户名和密码，以及程序的路径
user.prepare(
    user='', password='',
    exe_path='C:\\双子星-中国银河证券\\xiadan.exe'
)

# =====获取账户资金状况
balance = pd.DataFrame(user.balance)
print('\n账户资金状况：')
print(balance)

# =====获取持仓
position_info = pd.DataFrame(user.position)
if position_info.empty:
    print('没有持仓')
    exit()
else:
    print(position_info)
time.sleep(1)

slippery_rate = 2 / 1000  # 设置下单运行的滑点

for index, row in position_info.iterrows():
    print()

    amount = row['当前持仓']
    security_code = row['证券代码']
    print('>' * 5, '准备下单卖出股票', row['证券代码'], amount, '<' * 5)

    try:
        result = user.sell_market(
            security_code, '%s' % amount
        )  # 这边可以优化买入数量
    except easytrader.exceptions.TradeError as e:
        print(security_code, '交易失败', str(e))
        continue

    print(security_code, '卖出股票成功：', result)

# =====获取今日委托
today_entrusts = pd.DataFrame(user.today_entrusts)
print('\n今日委托：')
print(today_entrusts)

# =====查看今日成交
today_trades = pd.DataFrame(user.today_trades)
print('\n今日成交：')
print(today_trades)
