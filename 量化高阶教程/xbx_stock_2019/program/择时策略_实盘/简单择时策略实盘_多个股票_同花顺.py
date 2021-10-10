"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

更新于：2021-02-26
主要是解决了之前版本无法成功运行的问题。

如果针对多个股票，根据策略进行实盘交易
"""
from datetime import datetime, timedelta
import easytrader
from program.择时策略_实盘.Trade_Function import *
from program.择时策略_实盘.Trade_Signal import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====需要手工调整的参数
# 监控股票，及分配参数，建议不要满仓，最多到0.95，剩余就是现金
# 若账户持有不监控的股票，不会管
stock_df = pd.DataFrame(
    {
        'sh601288': {'分配仓位': 0.2},
        'sh601258': {'分配仓位': 0.1},
        'sz000002': {'分配仓位': 0.2},
    }
).T
strategy_para = [10, 20]  # 策略参数
run_interval = '15T'  # 程序运行周期，30T代表30分钟，如果是1小时就是1H。不要太低，不要低于5分钟
# 历史数据地址
hist_data_path = r'C:\Users\Markowitz\Desktop\1_xbx_stock_2021-pro\data\股票数据库\stock'
dingding_robot_id = ''  # 钉钉id

# =====固定参数
kline_num = max(strategy_para) + 5  # 获取的历史数据的数量
slippage = 1 / 100  # 下单价格偏移量

# =====初始化监控股票相关数据
hist_data_dict = {}  # 存放历史数据的dict
for stock_code in stock_df.index:
    stock_df.loc[stock_code, '股票代码'] = stock_code
    stock_df.loc[stock_code, '交易代码'] = stock_code[2:]
    # 股票今天是否可以交易
    stock_df.loc[stock_code, '是否交易'] = True
    # 股票的涨跌停价格
    stock_df.loc[stock_code, '涨停价格'], stock_df.loc[stock_code, '跌停价格'] = get_today_limit_from_eastmoney(stock_code)
    # 从本地文件中读取股票历史数据
    hist_data_dict[stock_code] = get_hist_candle_data(stock_code, kline_num=kline_num, folder_path=hist_data_path)
stock_df.set_index(keys='交易代码', inplace=True, drop=False)

# =====初始化同花顺自动交易系统
ths = easytrader.use('ths')
ths.connect(r'C:\同花顺软件\同花顺\xiadan')  # 填入交易客户端的路径。即安装目录下的 xiadan.exe 的地址
ths.enable_type_keys_for_editor()  # 不设置这个模式会有问题，无法录入股票代码、价格和数量


# =====主函数
def main(stock_df):
    print('=' * 5, '本次运行开始', datetime.now())
    if_trade = True

    # ===更新账户信息
    balance_dict, stock_df = update_account_data(ths, stock_df)

    # ===计算下一次执行的时间并且等待，针对股市收盘时间做了修正
    run_time = next_run_time(run_interval)  # 获取下次运行的时间
    # 判断run_time是否临近收盘
    if run_time.hour == 14 and run_time.minute > 55:  # 下午收盘，提前几分钟
        if_trade = True
    # sleep直至需要运行的时间附近
    time.sleep(max(0, (run_time - datetime.now()).seconds))
    while True:  # 在靠近目标时间时
        if datetime.now() >= run_time:
            break

    # ===获取监控股票的最新交易数据
    stock_code_list = list(stock_df['股票代码'].dropna())
    latest_df = get_today_data_from_sinajs(code_list=stock_code_list)
    print('最新股票数据：\n', latest_df, '\n')

    # ===遍历所有股票，判单每个股票的交易信号
    buy_stock_list = []
    sell_stock_list = []
    for stock_code in stock_code_list:
        # 合并历史数据数据，获取最近n根k线
        t = latest_df[latest_df['股票代码'] == stock_code]
        df = hist_data_dict[stock_code].append(t, ignore_index=True, sort=False)
        df.drop_duplicates(subset=['交易日期'], keep='last', inplace=True)
        # 计算复权价格
        df = cal_fuquan_price(df, fuquan_type='后复权')
        # 产生交易信号
        signal = Trade_simple_moving_average_signal(df, para=strategy_para)
        # signal = Trade_test_signal()
        if signal == 1 and stock_df.loc[stock_code[2:], '股票余额'] == 0:
            buy_stock_list.append(stock_code)
        elif signal == 0 and stock_df.loc[stock_code[2:], '可用余额'] > 0:
            sell_stock_list.append(stock_code)

    # ===创建丁丁消息
    dd_msg = ''
    dd_msg += '本周期需要买入的股票：\n%s\n' % str(buy_stock_list)
    dd_msg += '本周期需要卖出的股票：\n%s\n' % str(sell_stock_list)
    print(dd_msg)

    # ===卖出交易
    if sell_stock_list and if_trade:
        # 逐个卖出股票
        for stock_code in sell_stock_list:
            print('准备下单卖出股票：', stock_code)
            buy1_price = latest_df[latest_df['股票代码'] == stock_code].iloc[-1]['buy1']
            order_price = cal_order_price('sell', buy1_price, None, slippage, stock_df.loc[stock_code[2:], '涨停价格'],
                                          stock_df.loc[stock_code[2:], '跌停价格'])
            # 下单
            amount = stock_df.loc[stock_code[2:], '可用余额']
            # amount = 100
            order_info = ths.sell(ths, code=stock_code[2:], price=order_price, amount=amount)
            print('卖出股票成功：', order_info)
            time.sleep(0.5)

    # ===买入交易
    if buy_stock_list and if_trade:
        # 若之前有卖出交易，需要更新一下账户信息
        if sell_stock_list and if_trade:
            balance_dict, stock_df = update_account_data(ths, stock_df)

        # 逐个买入股票
        for stock_code in buy_stock_list:
            print('准备下单买入股票：', stock_code)
            # 计算买入价格
            sell1_price = latest_df[latest_df['股票代码'] == stock_code].iloc[-1]['sell1']
            order_price = cal_order_price('buy', None, sell1_price, slippage, stock_df.loc[stock_code[2:], '涨停价格'],
                                          stock_df.loc[stock_code[2:], '跌停价格'])
            # 计算买入数量
            buy_money = stock_df.loc[stock_code[2:], '分配资金']
            buy_amount = int(buy_money / order_price / 100) * 100
            print('买入数量', buy_amount)
            # buy_amount = 100
            if buy_amount >= 100:
                # 下单
                order_info = ths.buy(stock_code[2:], order_price, buy_amount)
                print('买入股票成功：', order_info)
                time.sleep(0.5)
            else:
                print('买入股票数量小于100股，无法买入')

    # ===更新账户信息
    time.sleep(5)  # 刚刚交易完，需要休息一段时间再获取数据
    balance_dict, stock_df = update_account_data(ths, stock_df)
    dd_msg += '账户资金状况：\n%s\n' % str(balance_dict)
    dd_msg += '股票持仓情况：\n%s\n' % str(stock_df[['分配仓位', '股票余额', '参考盈亏']])

    # ===发送消息，当有卖卖交易、收市之前、30分时，发钉钉消息
    if buy_stock_list or sell_stock_list or run_time.minute % 5 != 0 or run_time.minute % 30 == 0:
        send_dingding(dd_msg, robot_id=dingding_robot_id)

    # 本次交易结束
    time.sleep(5)
    print('=' * 5, '本次运行完毕:', datetime.now(), '\n\n')


# =====程序执行主体
while True:
    try:
        main(stock_df)
    except Exception as e:
        # 如果遇到报错，自动重试
        error_msg = '系统出错，10s之后重新运行，报错内容：%s' % e
        send_dingding(error_msg, robot_id=dingding_robot_id)
        print(error_msg)
        time.sleep(10)
