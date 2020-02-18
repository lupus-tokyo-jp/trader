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
        print('trade runnning.')
        tickers = self.getTickerAll()
        print(tickers)
        # depths = self.getDepthAll()
        # pprint.pprint(depths)
        # print(depths)
        trading_route = self.getTradingRoute(tickers)
        print(trading_route)

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
                    buy.setdefault("Coinckeck", int(val["bid"]))
                    sell.setdefault("Coinckeck", int(val["ask"]))

                else:
                    continue

            route['buy'] = min(sell, key=sell.get)
            route['sell'] = max(buy, key=buy.get)

        return route


