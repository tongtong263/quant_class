"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

课程中自定制的库已经删除，新版中使用
- 最新版本的同花顺客户端：http://activity.ths123.com/html/free/150324/
- Python3.8
- 最新版本的easytrader：pip install easytrader -i https://pypi.tuna.tsinghua.edu.cn/simple


完整实验整个交易流程，进行多次循环尝试：
1. 账户余额查询
2. 持仓查询
3. 限价买入股票
4. 撤单
5. 查询当日委托
6. 查询今日成交
"""
import warnings
import time
import easytrader  # 导入自动交易的库
import pandas as pd

pd.set_option('expand_frame_repr', False)


# =====创建自动下单对象
# 使用同花顺客户端进行下单
ths = easytrader.use('ths')
# 填入交易客户端的路径。即安装目录下的xiadan.exe的地址
ths.connect(r'C:\同花顺软件\同花顺\xiadan')
ths.enable_type_keys_for_editor()  # 不设置这个模式会有问题，无法录入股票代码、价格和数量

stock_code = '600823'
buy_price = 5.0

# 循环整个流程n次
for _ in range(3):
    print('*' * 10, '开始本次下单测试循环', '*' * 10)

    # =====获取账户资金状况
    print('\n账户资金状况：')
    balance_info = ths.balance
    print(balance_info)
    time.sleep(2)

    # =====获取持仓
    print('\n账户持仓状况：')
    position_info = pd.DataFrame(ths.position)
    if position_info.empty:
        print('没有持仓')
    else:
        print(position_info)
    time.sleep(1)

    # =====下单交易：限价买单
    print('\n准备下单买入股票：')
    order_info = ths.buy(stock_code, buy_price, '100')
    print('买入股票成功：', order_info)
    time.sleep(1)

    # =====撤单
    print('\n准备撤单买入的股票：')
    order_num = order_info.get('entrust_no') if order_info else None
    cancel_info = ths.cancel_entrust(order_num)
    print('撤单成功：', cancel_info)
    time.sleep(1)

    # =====撤单后查询当日委托
    print('\n准备查询当日所有的委托：')
    entrust_info = pd.DataFrame(ths.today_entrusts)
    if entrust_info.empty:
        print('没有委托')
    else:
        print(entrust_info)
    time.sleep(1)

    # =====查看今日成交
    print('\n准备查询当日所有的成交：')
    trade_info = pd.DataFrame(ths.today_trades)
    if trade_info.empty:
        print('没有成交记录')
    else:
        print(trade_info)

    print('本次下单测试循环结束', '\n' * 3)
    time.sleep(10)

"""
>>>> 重要注意事项 <<<<
1. xiadan.exe程序可能会崩溃，重新启动即可。建议每天开盘前重启xiadan.exe
2. 运行过程中不要把交易窗口最小化或者关闭,不要使用鼠标干预。
3. 关闭其他不用软件，例如360杀毒等。保持环境整洁。
4. 运行前切换为英文输入法。
5. 因为每个人的电脑环境问题，不是所有人都能正常运行，有任何问题请联系助教。
"""