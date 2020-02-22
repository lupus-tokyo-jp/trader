# encode=UTF-8
import sys
import logging
import pprint
import json
import importlib

import env
import classes.api.BitBank
import classes.api.CoinCheck

class Base:

    def __init__(self):
        self.Testing = 0
        self.Testing_route_buy = 'BitBank'
        self.Testing_route_sell = 'CoinCheck'

        environment = env.environment()
        self.config = environment.config()
        self.exchanges = environment.exchanges

        self.BitBank = classes.api.BitBank.BitBankAPI()
        self.CoinCheck = classes.api.CoinCheck.CoinCheckAPI()

    def trade(self):
        logging.info('> trade runnning > ')

        tickers = self.getTickerAll()
        print('> func trade > tickers: ' + json.dumps(tickers))
        logging.info('> func trade > tickers: ' + json.dumps(tickers))

        trading_route = self.getTradingRoute(tickers)
        print('> func trade > trading_route: ' + json.dumps(trading_route))
        logging.info('> func trade > trading_route: ' + json.dumps(trading_route))

        # テスト：売買固定
        if self.Testing:
            trading_route['buy'] = self.Testing_route_buy
            trading_route['sell'] = self.Testing_route_sell

            print('> func trade > TEST: route change > ' + json.dumps(trading_route))
            logging.info('> func trade > TEST: route change > ' + json.dumps(trading_route))

        if len(trading_route) and trading_route['buy'] != trading_route['sell']:
            msg = trading_route['buy'] + 'から購入して' + trading_route['sell'] + 'で売却します'
            pprint.pprint(msg)
            logging.info(msg)
        else:
            print('> func trade > route check : route not found')
            logging.info('> func trade > route check : route not found')
            sys.exit()

        # 売買
        for case, exch in trading_route.items():
            result = self.tradeRequests(case, exch)
            print('> func trade > ' + case + '_result >>> ' + json.dumps(result))
            logging.info('> func trade > ' + case + '_result >>> ' + json.dumps(result))

    def getTickerAll(self):
        tickers = {}
        tickers['Bitbank'] = self.BitBank.getTicker()
        tickers['CoinCheck'] = self.CoinCheck.getTicker()

        return tickers

    def getDepthAll(self):
        depths = {}
        depths['BitBank'] = self.BitBank.getDepth()
        depths['CoinCheck'] = self.CoinCheck.getOrderbooks()

        return depths

    def getTradingRoute(self, tickers):
        route = {}

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
                route['buy'] = min(sell, key=sell.get)
                route['sell'] = max(buy, key=buy.get)

        return route

    # type(sell or buy)
    # exch = BitCoin, CoinCheck...
    def tradeRequests(self, case: str, exch: str):
        result = ""
        cases = {
            'sell' : 'postSell',
            'buy' : 'postBuy'
        }
        if exch in self.exchanges and case in cases:
            class_name = exch + 'API'
            module = importlib.import_module('classes.api.' + exch, 'classes.api')
            exch_class = getattr(module, class_name)()
            result = getattr(exch_class, cases[case])()
            return result
        else:
            return "false"
