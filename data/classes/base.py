# encode=UTF-8
import sys
import pprint
import json
import time
import importlib

import env
import classes.utility
import classes.api.BitBank
import classes.api.CoinCheck
from enum import Enum, auto

class ValueNotIncludedType(Enum):
    MAX = auto()
    MIN = auto()

class Base:

    def __init__(self):
        self.cls_n = __class__.__name__

        # TEST.
        self.Testing = 0
        self.Testing_route_buy = 'BitBank'
        self.Testing_route_sell = 'CoinCheck'

        # Load env.
        environment = env.environment()
        self.config = environment.config()
        self.exchanges = environment.exchanges
        self.amount = environment.amount

        # Load utility.
        self.util = classes.utility.Utility()

        # Load API.
        self.BitBank = classes.api.BitBank.BitBankAPI()
        self.CoinCheck = classes.api.CoinCheck.CoinCheckAPI()

    def trade(self):
        trade_start = time.time()
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'trade runnning >>>> ')

        tickers = self.getTickerAll()
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, tickers)

        trading_route = self.getTradingRoute(tickers)
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, trading_route)

        # テスト：売買固定
        if self.Testing:
            trading_route['buy']['exchange'] = self.Testing_route_buy
            trading_route['sell']['exchange'] = self.Testing_route_sell

            self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, '[TEST] route change > ' + json.dumps(trading_route))

        if len(trading_route) and trading_route['buy']['exchange'] == trading_route['sell']['exchange']:
            self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'route not found')
            sys.exit()

        msg = trading_route['buy']['exchange'] + 'から購入して' + trading_route['sell']['exchange'] + 'で売却します'
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, msg)

        depths = self.getDepthAll()
        trading_data = self.depthArrayFormat(depths, trading_route)
        print(trading_data)
        sys.exit()

        # TEST用：売買の値
        trading_route['buy']['amount'] = 10
        trading_route['buy']['price'] = 11000
        trading_route['sell']['amount'] = 33
        trading_route['sell']['price'] = 33000

        # 売買
        for case, exch in trading_route.items():
            result = self.tradeRequests(case, exch['exchange'], exch['amount'], exch['price'])
            self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'trade result > ' + case + ' > ' + json.dumps(result))

        trade_time = time.time() - trade_start
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'trade time > ' + str(trade_time) + 'sec')

    # 全ての取引所のティッカーを取得する
    def getTickerAll(self):
        tickers = {}
        tickers['Bitbank'] = self.BitBank.getTicker()
        tickers['CoinCheck'] = self.CoinCheck.getTicker()

        return tickers

    # 全ての取引所の板情報を取得する
    def getDepthAll(self):
        depths = {}
        depths['BitBank'] = self.BitBank.getDepth()
        depths['CoinCheck'] = self.CoinCheck.getOrderbooks()

        return depths

    # valueNotIncludedに渡す配列を作成
    # asks 売り注文の情報
    # bids 買い注文の情報
    def depthArrayFormat(self, depths, trading_route):
        ary = {}
        for t_side, t_exch in trading_route.items():
            if t_side == 'buy':
                trading_route[t_side]['depth'] = self.removeAmount(depths[t_exch['exchange']]['asks'])
            elif t_side == 'sell':
                trading_route[t_side]['depth'] = self.removeAmount(depths[t_exch['exchange']]['bids'])
            else:
                continue

        return trading_route

    # depthの配列[price, amount]のamountを削る
    def removeAmount(self, depth):
        ary = []
        for val in depth:
            num = val[0]
            if not isinstance(num, int):
                num = int(float(val[0]))
            ary.append(num)

        return ary

    # どこの取引所で売買するのか決定する
    # return route = {'buy': {'exchange': 最小の売値の取引所名}, 'sell': {'exchange': 最大の買値の取引所名}}
    def getTradingRoute(self, tickers):
        route = {
            'buy': {},
            'sell': {}
        }

        if len(tickers) >= 2:
            buy = {}
            sell = {}

            for exch, val in tickers.items():
                if exch == 'Bitbank':
                    buy.setdefault("BitBank", int(val['data']["buy"]))
                    sell.setdefault("BitBank", int(val['data']["sell"]))

                elif exch == 'CoinCheck':
                    buy.setdefault("CoinCheck", int(val["bid"]))
                    sell.setdefault("CoinCheck", int(val["ask"]))

                else:
                    continue

            if len(sell) and len(buy):
                route['buy']['exchange'] = min(sell, key=sell.get)
                route['sell']['exchange'] = max(buy, key=buy.get)

        return route

    # 売買の実行
    # case = sell or buy
    # exch = BitCoin, CoinCheck...
    # amount int 数量
    # price int 金額
    def tradeRequests(self, case: str, exch: str, amount: int, price: int):
        result = ""
        cases = {
            'sell' : 'postSell',
            'buy' : 'postBuy'
        }

        if exch in self.exchanges and case in cases:
            class_name = exch + 'API'
            module = importlib.import_module('classes.api.' + exch, 'classes.api')
            exch_class = getattr(module, class_name)()
            result = getattr(exch_class, cases[case])(amount, price)
            return result

        return None

    # 配列内の最小値または最大値を取得する
    # args: 最小値を求める時は昇順, 最大値を求める時は降順にソートした配列
    # type: 最小値を求める時は .MIN, 最大値を求める時は .MAXを指定
    def valueNotIncluded(args: [int], type: ValueNotIncludedType, index: int):

        count = len(args)

        # 空配列は０を返す
        if count == 0:
            return 0

        # MINの時は 最小値から順に大きくして探すため +1
        if type == ValueNotIncludedType.MIN:
            d = 1
        # MAXの時は 最大値から順に小さくして探すため -1
        elif type == ValueNotIncludedType.MAX:
            d = -1

        # 要素１つの場合は 要素+d の値を返す
        if count == 1:
            return args[0] + d
        elif count == index:
            return args[0] + d


        min = args[index]
        print("asks: " + str(args))
        print("value: " + str(min) + ", check: " + str(min+d))

        if min + d == args[index+1]:
            print("...hit")
            return valueNotIncluded(args, type, index + 1)

        return min + d
