# encode=UTF-8
import logging
import pprint
import json

import classes.api.BitBank
import classes.api.CoinCheck

class Base:

    def __init__(self):
        self.BitBank = classes.api.BitBank.BitBankAPI()
        self.CoinCheck = classes.api.CoinCheck.CoinCheckAPI()

    def trade(self):
        logging.info('trade runnning > ')

        tickers = self.getTickerAll()
        print(tickers)
        logging.info('func trade > tickers: ' + json.dumps(tickers))

        trading_route = self.getTradingRoute(tickers)
        print(trading_route)
        logging.info('func trade > trading_route: ' + json.dumps(trading_route))

        if len(trading_route):
            pprint.pprint(trading_route['buy'] + 'から購入して' + trading_route['sell'] + 'で売却します')

        print('TEST: route change >')
        trading_route['buy'] = 'BitBank'
        trading_route['sell'] = 'CoinCheck'
        print(trading_route)

        # 買う
        buy_result = self.purchase(str(trading_route['buy']))
        pprint.pprint(buy_result)
        logging.info('func trade > buy_result: ' + buy_result)

        # 売る
        sell_result = self.sell(str(trading_route['sell']))
        pprint.pprint(sell_result)
        logging.info('func trade > sell_result: ' + sell_result)



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

    def purchase(self, exch_buy: str):
        result = ""

        if exch_buy == 'BitBank':
            result = self.BitBank.postBuy()

        elif exch_buy == 'CoinCheck':
            result = self.CoinCheck.postBuy()

        else:
            result = ""

        return result

    def sell(self, exch_sell: str):
        result = ""

        if exch_sell == 'BitBank':
            result = self.BitBank.postSell()

        elif exch_sell == 'CoinCheck':
            result = self.CoinCheck.postSell()

        else:
            result = ""

        return result
