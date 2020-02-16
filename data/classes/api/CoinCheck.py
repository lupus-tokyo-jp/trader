# encode=UTF-8
import logging
import pprint
import json

import coincheck.order, market, account

class CoinCheckAPI:
    def __init__(self):
        self.order = coincheck.order.Order()
        self.market = coincheck.market.Market()
        self.order = coincheck.order.Order()

    # Public API
    def getTicker(self):
        value = self.market.ticker.all()
        # print(json.dumps(value))
        return value

    # Public API
    def getTrade(self):
        value = self.market.trade.all()
        print(json.dumps(value))

    # Public API
    def getOrderbook(self):
        value = self.market.order_book()
        # print(json.dumps(value))
        return value
