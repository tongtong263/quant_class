"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

更新于：2020-12-17
主要是解决了之前版本无法成功运行的问题。
课程中自定制的库已经删除，新版中使用
- 最新版本的同花顺客户端：http://activity.ths123.com/html/free/150324/
- Python3.8
- 最新版本的easytrader：pip install easytrader -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
import easytrader  # 导入自动交易的库
import pandas as pd

pd.set_option('expand_frame_repr', False)


# =====创建自动下单对象
# 使用同花顺客户端进行下单
ths = easytrader.use('ths')
# 填入交易客户端的路径。即安装目录下的xiadan.exe的地址
ths.connect(r'C:\同花顺软件\同花顺\xiadan.exe')
ths.enable_type_keys_for_editor()  # 不设置这个模式会有问题，无法录入股票代码、价格和数量

# =====获取账户资金状况
balance_info = ths.balance
print(balance_info)
print(balance_info['资金余额'])  # 返回结果是一个dict

# =====获取持仓
# position_info = pd.DataFrame(ths.position)
# if position_info.empty:
     # print('没有持仓')
# else:
     # print(position_info)  # 返回结果是一个DataFrame

# =====下单交易
# ===限价买单
# order_info = ths.buy('600000', '9.78', '100')
# print(order_info)  # 返回order_id，即为合同编号：{'entrust_no': '74671'}
# order_num = order_info['entrust_no']
# print('订单编号：', order_num)

# ===下单特殊情况
# 未上市、停牌、退市的股票无法操作，尝试600001，提交失败：-990221020[-990221020]无此证券代码!
# 委托股数不对：easytrader.exceptions.TradeError: 提交失败：-150904070[-150904070] 委托数量必须是每手股(张)数的倍数。
# 委托价格最多小数点后两位，精度太高，会四舍五入。例如 5.423会取整为5.42
# 不能提交低于跌停价，高于涨停价的价格: 提交失败：-990265060[-990265060]委托价格超过涨停价格。
# 资金余额不够，尝试600519：提交失败：-150906130[-150906130]资金可用数不足,尚需322944.07。
# 不在交易时间，提交失败：-990297020[-990297020]当前时间不允许做该项业务。
# 断网会直接报错

# ===限价卖单，同买单一样
# order_info = ths.sell('600000', '9.78', '100')

# ===市价单，不需要填价格
# order_info = ths.market_buy('600789', '100')
# order_info = ths.market_sell('600789', '100')

# =====撤单
# order_num = '150576'
# cancel_info = ths.cancel_entrust(order_num)
# print(cancel_info)  # {'message': '您的撤单委托已成功提交，合同编号：104332。'}

# =====查询订单
# 查看今日所有的委托
entrust_info = pd.DataFrame(ths.today_entrusts)
if entrust_info.empty:
    print('今日没有委托')
else:
    print(entrust_info)

# 查看今日所有订单
trade_info = pd.DataFrame(ths.today_trades)
if trade_info.empty:
    print('今日没有订单')
else:
    print(trade_info)
