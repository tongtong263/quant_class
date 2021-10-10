"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

演示各个下单操作
"""
import easytrader
import pandas as pd

pd.set_option('expand_frame_repr', False)

# =====创建自动下单对象
user = easytrader.use('yh_client')  # 选择银河客户端

# 输入用户名和密码，以及程序的路径
user.prepare(
    user='', password='',
    exe_path='C:\\双子星金融终端-中国银河证券\\xiadan.exe'
)

# =====获取账户资金状况
balance = pd.DataFrame(user.balance)
print('\n账户资金状况：')
print(balance)

# =====获取持仓
position_info = pd.DataFrame(user.position)
if position_info.empty:
    print('没有持仓')
else:
    print(position_info)

# =====下单交易
# ===限价买单
order_info = user.buy('600823', 5, 100)  # 600823
print(order_info)  # 返回order_id，即为合同编号：{'entrust_no': '74671'}
order_num = order_info['entrust_no']
print('订单编号：', order_num)

# ===下单特殊情况
# 未上市、停牌、退市的股票无法操作，尝试600001，提交失败：-990221020[-990221020]无此证券代码!
# 委托股数不对：easytrader.exceptions.TradeError: 提交失败：-150904070[-150904070] 委托数量必须是每手股(张)数的倍数。
# 委托价格最多小数点后两位，精度太高，会四舍五入。例如 5.423会取整为5.42
# 不能提交低于跌停价，高于涨停价的价格: 提交失败：-990265060[-990265060]委托价格超过涨停价格。
# 资金余额不够，尝试600519：提交失败：-150906130[-150906130]资金可用数不足,尚需322944.07。
# 不在交易时间，提交失败：-990297020[-990297020]当前时间不允许做该项业务。
# 断网会直接报错

# ===限价卖单，同买单一样
order_info = user.sell('000005', 0.55, 100)

# ===市价单，不需要填价格
order_info = user.market_buy('600823', 100)
order_info = user.market_sell('600823', 100)

# =====撤单
order_num = '150576'
cancel_info = user.cancel_entrust(order_num)
print(cancel_info)  # {'message': '您的撤单委托已成功提交，合同编号：104332。'}

# =====查询订单
# 查看今日所有的委托
entrust_info = pd.DataFrame(user.today_entrusts)
if entrust_info.empty:
    print('今日没有委托')
else:
    print(entrust_info)

# 查看今日所有订单
trade_info = pd.DataFrame(user.today_trades)
if trade_info.empty:
    print('今日没有订单')
else:
    print(trade_info)
