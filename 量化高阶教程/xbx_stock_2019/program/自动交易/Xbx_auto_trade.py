"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

邢不行封装各个自动交易接口，本程序禁止任何修改

- `xbx_`开头的函数都是给自动交易准备的
- `_`开头的函数是辅助函数
- 默认最大试错次数为5次
- 调用方法参考文件：案例_下单接口介绍.py
"""
import time

import pandas as pd

from easytrader_xingbuxing.clienttrader import ClientTrader
from easytrader_xingbuxing.exceptions import TradeError

DEFAULT_MAX_TRY = 5


def _run_with_auto_rerun(cli: ClientTrader, max_try_count, name, func, *args):
    """
    带有自动重试机制的运行
    :param cli: 客户端对象
    :param max_try_count: 最大尝试的次数
    :param name: 程序的名字
    :param func: 需要运行的程序
    :param args: 输入的参数
    """
    try_count = 0
    while try_count < max_try_count:
        try:
            rt = func(*args)
            if rt is not None:
                cli.clear()
                return rt
        except Exception as e:
            print('[%s报错]' % name, e)
        try_count += 1
        cli.clear()
        time.sleep(0.2)

    raise ValueError(('[%s操作不断报错，达到最大尝试次数，请尽快检查并修复]' % name))


def _trade(cli, func, max_try_count, **kwargs):
    """
    交易核心函数
    :param cli: 客户端
    :param func: 执行函数（买卖或者市价买卖）
    :param max_try_count: 最大试错次数
    :param kwargs: 交易用参数
    :return: 交易结果
    """
    try_count = 0
    while try_count < max_try_count:
        try:
            trade_result = func(**kwargs)  # 返回结果是一个{'entrust_no': '122631'}
            if 'entrust_no' in trade_result:
                cli.clear()
                return trade_result
            else:
                print('[交易出错]，出错原因：返回结果不包含entrust_no，返回结果为：', str(trade_result))
                cli.clear()
            # # ===处理极端情况下回执为空的情况
            # entrust_no = None
            # if trade_result:
            #     entrust_no = trade_result.get('entrust_no')
            # if not entrust_no:
            #     entrusts = xbx_get_today_pending_entrusts(cli)
            #     trade_result = dict(entrust_no=entrusts.iloc[-1]['合同编号'])
            return trade_result
        except TradeError as te:
            print('[交易失败]，失败原因：', te,  '重试')
            cli.clear()
            break
        except Exception as e:
            print('[交易出错]，出错原因：', e, '重试')
            cli.clear()
        try_count += 1
        time.sleep(0.2)

    raise ValueError('尝试下单，不断失败，达到尝试次数上限，请尽快检查并修复')


def xbx_get_balance(cli: ClientTrader, max_try_count=DEFAULT_MAX_TRY) -> dict:
    """
    获取账户信息
    :param cli: 客户端
    :param max_try_count: 最大试错次数
    :return: 包含账户信息的字典dict
    {'资金余额': 225936.09, '可用金额': 225964.25, '可取金额': 225936.09, '股票市值': 0.0, '总资产': 225964.25}
    """
    def _do():
        balance = cli.balance
        if '总资产' in balance:
            return balance
        else:
            return None

    return _run_with_auto_rerun(cli, max_try_count, '获取账户余额', _do)


def xbx_get_position(cli: ClientTrader, max_try_count=DEFAULT_MAX_TRY) -> pd.DataFrame:
    """
    获取持仓
    :param cli: 客户端
    :param max_try_count: 最大试错次数
    :return: 包含持仓信息的DataFrame
     Unnamed: 18    买入成本  交易市场  冻结数量  单位数量   参考成本价    参考盈亏  参考盈亏比例(%)  可用余额  实际数量     市价      市值  市场代码 明细        股东帐户  股票余额    证券代码  证券名称 资讯
0               3.082  上海Ａ股     0     0   3.082  158.11     17.132   300   300   3.61  1083.0     2     A790558087   300  601288  农业银行
1              30.662  上海Ａ股     0     0  30.662  256.55      8.375   100   100  33.23  3323.0     2     A790558087   100  601601  中国太保

    """
    def _do():
        position = pd.DataFrame(cli.position)
        if '可用余额' in position.columns or position.empty:
            return position
        else:
            return None

    return _run_with_auto_rerun(cli, max_try_count, '获取持仓', _do)


def xbx_get_today_entrusts(cli: ClientTrader, max_try_count=DEFAULT_MAX_TRY) -> pd.DataFrame:
    """
    获取今日委托订单信息
    :param cli: 客户端
    :param max_try_count: 最大试错次数
    :return: 包含订单信息的DataFrame
    """
    def _do():
        entrusts = cli.today_entrusts
        entrusts = pd.DataFrame(entrusts)
        if '备注' in entrusts.columns or entrusts.empty:
            return entrusts
        else:
            return None

    return _run_with_auto_rerun(cli, max_try_count, '获取今日委托', _do)


def xbx_get_today_trades(cli: ClientTrader, max_try_count=DEFAULT_MAX_TRY) -> pd.DataFrame:
    """
    获取今日成交
    :param cli: 客户端
    :param max_try_count: 最大试错次数
    :return: 包含成交信息的DataFrame
    """
    def _do():
        trades = cli.today_trades
        trades = pd.DataFrame(trades)
        if '成交编号' in trades.columns or trades.empty:
            return trades
        else:
            return None

    return _run_with_auto_rerun(cli, max_try_count, '获取今日成交', _do)


def xbx_get_today_pending_entrusts(cli: ClientTrader, entrusts: pd.DataFrame = None,
                                   max_try_count=DEFAULT_MAX_TRY) -> pd.DataFrame:
    """
    获取今日未成交的委托订单信息
    :param cli: 客户端
    :param entrusts: (可选参数)已经获取的当日委托，如果为None，会自动获取最新的当日委托
    :param max_try_count: 最大试错次数
    :return: 包含当日未成交委托信息的DataFrame
    """
    def _do(_entrusts):
        if _entrusts is None:
            _entrusts = xbx_get_today_entrusts(cli)
        return entrusts[entrusts['备注'].str.contains('已报')]

    return _run_with_auto_rerun(cli, max_try_count, '获取今日未成交委托', _do, entrusts)


def xbx_buy(cli: ClientTrader, code, price, amount, max_try_count=DEFAULT_MAX_TRY):
    """
    限价买入。若下单失败，会继续尝试下单，最多尝试次数：max_try_count
    如果下单成功，返回结果中一定是包含entrust_no的dict，例如{'entrust_no': '74671'}
    :param cli: 客户端
    :param code: 买入股票的代码，字符串，只需要6位数字代码，例如'000002'
    :param price: 价格，浮点数，例如5.28
    :param amount: 数量，整数，100的整数倍，例如300
    :param max_try_count: 最大试错次数
    :return: 交易结果，dict，{'entrust_no': '74671'}，合同编号
    """
    return _trade(cli, cli.buy, max_try_count, security=code, price=price, amount=amount)


def xbx_sell(cli: ClientTrader, code, price, amount, max_try_count=DEFAULT_MAX_TRY):
    """
    限价卖出
    :param cli: 客户端
    :param code: 股票代码
    :param price: 价格
    :param amount: 数量
    :param max_try_count: 最大试错次数
    :return: 交易结果
    """
    return _trade(cli, cli.sell, max_try_count, security=code, price=price, amount=amount)


def xbx_market_buy(cli: ClientTrader, code, amount, max_try_count=DEFAULT_MAX_TRY):
    """
    市价买入
    :param cli: 客户端
    :param code: 股票代码
    :param amount: 数量
    :param max_try_count: 最大试错次数
    :return: 交易结果
    """
    return _trade(cli, cli.buy, max_try_count, security=code, amount=amount)


def xbx_market_sell(cli: ClientTrader, code, amount, max_try_count=DEFAULT_MAX_TRY):
    """
    市价卖出
    :param cli: 客户端
    :param code: 股票代码
    :param amount: 数量
    :param max_try_count: 最大试错次数
    :return: 交易结果
    """
    return _trade(cli, cli.sell, max_try_count, security=code, amount=amount)


def xbx_cancel_entrust(cli: ClientTrader, entrust_no, max_try_count=DEFAULT_MAX_TRY):
    """
    撤单
    :param cli: 客户端
    :param entrust_no: 撤单的单号，字符串，例如： '103955'
    :param max_try_count: 最大试错次数
    :return: 撤单结果
    """
    def _do(_entrust_no):
        cancel_result = cli.cancel_entrust(_entrust_no)
        if cancel_result and 'message' in cancel_result and '成功提交' in cancel_result['message']:
            return cancel_result
        else:
            print('[撤单失败]，失败原因：', cancel_result)
            return None

    return _run_with_auto_rerun(cli, max_try_count, '撤单', _do, entrust_no)
