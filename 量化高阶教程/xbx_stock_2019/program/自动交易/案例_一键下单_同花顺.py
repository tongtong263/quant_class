"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

更新于：2021-02-26
新增一键下单-同花顺版本

一键买入十个股票，每个股票买入100股
"""
import easytrader
import pandas as pd
import time
import warnings

from program.构建自己的股票数据库.每日更新股票数据 import get_today_data_from_sinajs  # 需更改为本电脑路径及地址

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
else:
    print(position_info)
time.sleep(1)

# =====下单交易
stock_code_list = [
    'sh600010', 'sh600022', 'sh600157', 'sh600255', 'sh601258',
    'sh603077', 'sz002131', 'sz002509', 'sz002610', 'sz300116'
]
slippery_rate = 2 / 1000  # 设置下单运行的滑点
# 获取最新股价
price_df = get_today_data_from_sinajs(stock_code_list)

for stock_code in stock_code_list:
    security_code = stock_code[2:]  # 生成下单需要的证券代码
    print()
    print('>' * 5, '准备下单买入股票', security_code, '<' * 5)
    # 买入限价
    sell1_price = price_df[price_df['stock_code'] == stock_code].iloc[-1]['sell1']
    sell1_price = sell1_price * (1 + slippery_rate)  # 加入滑点价格

    try:
        result = ths.buy(
            security_code, '%s' % (round(sell1_price, 2)), '100'
        )  # 这边可以优化买入数量
    except easytrader.exceptions.TradeError as e:
        print(security_code, '交易失败', str(e))
        continue

    print(security_code, '买入股票成功：', result)

# =====获取今日委托
today_entrusts = pd.DataFrame(ths.today_entrusts)
print('\n今日委托：')
print(today_entrusts)

# =====查看今日成交
today_trades = pd.DataFrame(ths.today_trades)
print('\n今日成交：')
print(today_trades)
