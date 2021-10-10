"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

更新于：2021-02-26
新增一键空仓-同花顺版本

一键卖出十个卖出所有股票的所有持仓
"""
import easytrader
import pandas as pd
import time
import warnings

from program.构建自己的股票数据库.每日更新股票数据 import get_today_data_from_sinajs # 需更改为本电脑路径及地址

pd.set_option('expand_frame_repr', False)
warnings.filterwarnings("ignore")

# =====初始化同花顺自动交易系统
ths = easytrader.use('ths')
ths.connect(r'C:\同花顺软件\同花顺\xiadan')  # 填入交易客户端的路径。即安装目录下的 xiadan.exe 的地址
ths.enable_type_keys_for_editor()  # 不设置这个模式会有问题，无法录入股票代码、价格和数量


# =====获取账户资金状况
balance = pd.DataFrame(ths.balance)
print('\n账户资金状况：')
print(balance)

# =====获取持仓
position_info = pd.DataFrame(ths.position)
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
        result = ths.sell_market(
            security_code, '%s' % amount
        )  # 这边可以优化买入数量
    except easytrader.exceptions.TradeError as e:
        print(security_code, '交易失败', str(e))
        continue

    print(security_code, '卖出股票成功：', result)

# =====获取今日委托
today_entrusts = pd.DataFrame(ths.today_entrusts)
print('\n今日委托：')
print(today_entrusts)

# =====查看今日成交
today_trades = pd.DataFrame(ths.today_trades)
print('\n今日成交：')
print(today_trades)
