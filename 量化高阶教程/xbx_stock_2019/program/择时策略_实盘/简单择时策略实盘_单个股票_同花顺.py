"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

更新于：2021-02-26
主要是解决了之前版本无法成功运行的问题。

如果针对单个股票，根据策略进行实盘交易
"""
import easytrader
from 量化高阶教程.xbx_stock_2019.program.择时策略_实盘.Trade_Function import *
from 量化高阶教程.xbx_stock_2019.program.择时策略_实盘.Trade_Signal import *

from 量化高阶教程.xbx_stock_2019.program.择时策略_实盘.Trade_Function import get_today_limit_from_eastmoney

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====需要手工调整的参数
stock_code = 'sz002193'  # 监控的股票，也可以是ETF
max_buy_money = 100000  # 最多分配资金
strategy_para = [10, 20]  # 策略参数
run_interval = '15T'  # 程序运行周期，30T代表30分钟，如果是1小时就是1H。不要太低，不要低于5分钟
# 历史数据地址
hist_data_path = r'C:\Users\Markowitz\Desktop\1_xbx_stock_2021-pro\data\股票数据库\stock'  # 换成自己电脑的地址
dingding_robot_id = ''  # 换成自己的钉钉id

# =====固定参数
kline_num = max(strategy_para) + 5  # 获取的历史数据的数量
slippage = 1 / 100  # 下单价格偏移量

# =====初始化监控股票相关数据
stock_info = {
    '股票代码': stock_code,
    '交易代码': stock_code[2:],
    '最大买入资金': max_buy_money,
    '是否交易': True,  # 股票今天是否可以交易
}

# 股票的涨跌停价格，为什么不自己算，而是去网站上获取？
stock_info['涨停价格'], stock_info['跌停价格'] = get_today_limit_from_eastmoney(stock_code)

# 从本地文件中读取股票历史数据
hist_data = get_hist_candle_data(stock_code, kline_num=kline_num, folder_path=hist_data_path)

# =====初始化同花顺自动交易系统
ths = easytrader.use('ths')
ths.connect(r'C:\同花顺软件\同花顺\xiadan')  # 填入交易客户端的路径。即安装目录下的 xiadan.exe 的地址
ths.enable_type_keys_for_editor()  # 不设置这个模式会有问题，无法录入股票代码、价格和数量


# =====主函数
def main():
    print('=' * 5, '本次运行开始', datetime.now())
    if_trade = True

    # ===更新股票持仓信息
    update_one_stock_info(ths, stock_info)

    # # ===计算下一次执行的时间并且等待，针对股市收盘时间做了修正
    # run_time = next_run_time(run_interval)  # 获取下次运行的时间
    # # 判断run_time是否临近收盘
    # if run_time.hour == 14 and run_time.minute > 55:  # 下午收盘，提前几分钟
    #     if_trade = True
    # # sleep直至需要运行的时间附近
    # time.sleep(max(0, (run_time - datetime.now()).seconds))
    # while True:  # 在靠近目标时间时
    #     if datetime.now() >= run_time:
    #         break

    # ===获取最新交易数据
    latest_df = get_today_data_from_sinajs(code_list=[stock_info['股票代码']])
    print('最新股票数据：\n', latest_df, '\n')

    # ===判单股票的交易信号
    buy_stock = False
    sell_stock = False
    # =合并历史数据数据，获取最近n根k线
    df = hist_data.append(latest_df, ignore_index=True, sort=False)
    df.drop_duplicates(subset=['交易日期'], keep='last', inplace=True)
    # =计算复权价格
    df = cal_fuquan_price(df, fuquan_type='后复权')
    # =产生交易信号
    signal = Trade_simple_moving_average_signal(df, para=strategy_para)
    # signal = Trade_test_signal()
    # =判断实际信号
    # 当有买入信号，并且没有持有股票的时候，发出买入信号
    if signal == 1 and stock_info['股票余额'] == 0 and if_trade:
        buy_stock = True
    # 当有卖出信号，并且有股票可卖的时候，发出卖出信号
    elif signal == 0 and stock_info['可用余额'] > 0 and if_trade:
        sell_stock = True

    sell_stock = True

    # ===创建丁丁消息
    dd_msg = ''
    dd_msg += '本周期需要买入股票：%s\n' % str(buy_stock)
    dd_msg += '本周期需要卖出股票：%s\n' % str(sell_stock)
    print(dd_msg)

    # ===卖出交易
    if sell_stock:
        print('准备下单卖出股票')
        buy1_price = latest_df.iloc[-1]['buy1']
        order_price = cal_order_price('sell', buy1_price, None, slippage, stock_info['涨停价格'],
                                      stock_info['跌停价格'])
        # 下单
        sell_amount = stock_info['可用余额']
        # sell_amount = 100
        order_info = ths.buy(stock_info['交易代码'], '%.2f' % order_price, '%s' % int(sell_amount))
        print('卖出股票成功：', order_info)
        time.sleep(0.5)

    # ===买入交易
    if buy_stock:
        print('准备下单买入股票')
        # 计算买入价格
        print(latest_df)
        sell1_price = latest_df.iloc[-1]['sell1']
        order_price = cal_order_price('buy', None, sell1_price, slippage, stock_info['涨停价格'],
                                      stock_info['跌停价格'])
        # 计算买入数量
        buy_money = min(stock_info['最大买入资金'], stock_info['可用资金'])
        print(buy_money, order_price)
        buy_amount = int(buy_money / order_price / 100) * 100
        # buy_amount = 100
        if buy_amount >= 100:
            # 下单
            order_info = ths.buy(stock_info['交易代码'], '%.2f' % order_price, '%s' % int(buy_amount))
            print('买入股票成功：', order_info)
            time.sleep(0.5)
        else:
            print('买入股票数量小于100股，无法买入')

    # ===更新账户信息
    time.sleep(5)  # 刚刚交易完，需要休息一段时间再获取数据
    update_one_stock_info(ths, stock_info)
    dd_msg += '最新股票数据：\n%s\n' % str(stock_info)

    # # ===发送消息，当有卖卖交易、收市之前、30分时，发钉钉消息
    # if buy_stock or sell_stock or run_time.minute % 5 != 0 or run_time.minute % 30 == 0:
    #     send_dingding(dd_msg, robot_id=dingding_robot_id)

    # ===本次交易结束
    time.sleep(5)
    print('=' * 5, '本次运行完毕:', datetime.now(), '\n\n')


# =====程序执行主体
while True:
    try:
        main()
    except Exception as e:
        # 如果遇到报错，自动重试
        error_msg = '系统出错，10s之后重新运行，报错内容：%s' % e
        # send_dingding(error_msg, robot_id=dingding_robot_id)
        print(error_msg)
        time.sleep(10)
